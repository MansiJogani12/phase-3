"""
Repository Context Service - Phase 1
Fetches and caches repository data from GitHub, then selects relevant
files/metadata based on the user's query to build a targeted AI prompt.
"""
import httpx
import base64
import json
from typing import Optional

GITHUB_API = "https://api.github.com"

# Token budget: stay well under 100k chars to avoid hitting model context limits
MAX_CONTEXT_CHARS = 60_000
MAX_FILE_CHARS = 8_000  # per file


def _github_headers(token: Optional[str] = None) -> dict:
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def _fetch(url: str, token: Optional[str] = None, params: dict = None) -> dict | list | None:
    """Synchronous GitHub API fetch."""
    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.get(url, headers=_github_headers(token), params=params)
            if resp.status_code == 200:
                return resp.json()
            return None
    except Exception:
        return None


def _fetch_file_content(username: str, reponame: str, path: str, token: Optional[str] = None) -> Optional[str]:
    """Fetch a single file's decoded content from GitHub."""
    url = f"{GITHUB_API}/repos/{username}/{reponame}/contents/{path}"
    data = _fetch(url, token)
    if data and isinstance(data, dict) and data.get("encoding") == "base64":
        try:
            return base64.b64decode(data["content"]).decode("utf-8", errors="replace")
        except Exception:
            return None
    return None


# ─── Key file matchers ────────────────────────────────────────────────────────

PRIORITY_FILES = [
    "README.md", "README.rst", "README.txt",
    "package.json", "requirements.txt", "pyproject.toml",
    "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
    ".env.example", "go.mod", "Cargo.toml", "pom.xml",
    "build.gradle", "setup.py", "setup.cfg",
]

KEYWORD_GROUPS = {
    "auth": ["auth", "login", "oauth", "jwt", "token", "session", "passport", "guard", "middleware"],
    "deploy": ["docker", "deploy", "nginx", "workflow", "ci", "cd", "kubernetes", "k8s", "helm", "release"],
    "api": ["route", "controller", "endpoint", "api", "handler", "view", "schema"],
    "database": ["model", "schema", "migration", "database", "db", "mongo", "postgres", "sql", "redis"],
    "dependency": ["package.json", "requirements", "dependencies", "toml", "lock"],
    "security": ["security", "vulnerability", "cve", "permission", "rate.limit", "csrf", "xss", "sanitize"],
    "config": ["config", ".env", "setting", "constant", "environment"],
    "test": ["test", "spec", "jest", "pytest", "unittest"],
}


def _query_keywords(query: str) -> list[str]:
    """Extract relevant keyword groups from the user query."""
    q = query.lower()
    matched = []
    for group, keywords in KEYWORD_GROUPS.items():
        if any(kw in q for kw in keywords):
            matched.append(group)
    return matched


def _score_file(path: str, groups: list[str]) -> int:
    """Score a file path for relevance to the keyword groups."""
    p = path.lower()
    score = 0
    for group in groups:
        for kw in KEYWORD_GROUPS.get(group, []):
            if kw in p:
                score += 2
    # bonus for important extensions
    if p.endswith((".js", ".ts", ".py", ".go", ".rs", ".java")):
        score += 1
    # penalty for generated/lock/dist files
    if any(x in p for x in ["node_modules", ".min.", "dist/", "build/", "vendor/", "-lock.", ".lock"]):
        score -= 10
    return score


# ─── Main Service ─────────────────────────────────────────────────────────────

def build_repository_context(username: str, reponame: str, query: str, token: Optional[str] = None) -> str:
    """
    Build a targeted context string for the AI, grounded in real GitHub data.
    Returns a text block to inject into the system prompt.
    """
    context_parts = []

    # 1. Repository metadata
    repo_data = _fetch(f"{GITHUB_API}/repos/{username}/{reponame}", token)
    if repo_data:
        meta = (
            f"Repository: {repo_data.get('full_name', f'{username}/{reponame}')}\n"
            f"Description: {repo_data.get('description') or 'N/A'}\n"
            f"Language: {repo_data.get('language') or 'N/A'}\n"
            f"Stars: {repo_data.get('stargazers_count', 0)} | "
            f"Forks: {repo_data.get('forks_count', 0)} | "
            f"Open Issues: {repo_data.get('open_issues_count', 0)}\n"
            f"Default Branch: {repo_data.get('default_branch', 'main')}\n"
            f"License: {repo_data.get('license', {}).get('name', 'N/A') if repo_data.get('license') else 'N/A'}\n"
            f"Created: {repo_data.get('created_at', '')[:10]} | "
            f"Updated: {repo_data.get('updated_at', '')[:10]}\n"
            f"URL: {repo_data.get('html_url', '')}\n"
        )
        context_parts.append("=== REPOSITORY METADATA ===\n" + meta)

    # 2. File tree (top-level + one level deep to keep it manageable)
    tree_data = _fetch(
        f"{GITHUB_API}/repos/{username}/{reponame}/git/trees/{repo_data.get('default_branch', 'main') if repo_data else 'main'}",
        token,
        params={"recursive": "1"}
    )
    all_files = []
    if tree_data and "tree" in tree_data:
        all_files = [item["path"] for item in tree_data["tree"] if item["type"] == "blob"]
        # Show a compact summary of the file tree (limit to 150 paths)
        display_files = [p for p in all_files if not any(
            x in p for x in ["node_modules/", "dist/", ".min.", "vendor/"]
        )][:150]
        context_parts.append("=== FILE STRUCTURE (sample) ===\n" + "\n".join(display_files))

    # 3. Priority files (README, package.json, etc.)
    fetched_files = {}
    total_chars = sum(len(p) for p in context_parts)

    for priority_file in PRIORITY_FILES:
        if total_chars >= MAX_CONTEXT_CHARS:
            break
        # Check if file exists in tree
        matching = [f for f in all_files if f.lower() == priority_file.lower() or f.lower().endswith("/" + priority_file.lower())]
        if matching:
            path = matching[0]
            content = _fetch_file_content(username, reponame, path, token)
            if content:
                snippet = content[:MAX_FILE_CHARS]
                if len(content) > MAX_FILE_CHARS:
                    snippet += "\n... [truncated]"
                fetched_files[path] = snippet
                total_chars += len(snippet)

    # 4. Query-relevant files
    groups = _query_keywords(query)
    if groups and all_files:
        # Score all files
        scored = [(path, _score_file(path, groups)) for path in all_files]
        scored = sorted(scored, key=lambda x: x[1], reverse=True)
        top_relevant = [path for path, score in scored if score > 0][:8]

        for path in top_relevant:
            if total_chars >= MAX_CONTEXT_CHARS:
                break
            if path in fetched_files:
                continue
            content = _fetch_file_content(username, reponame, path, token)
            if content:
                snippet = content[:MAX_FILE_CHARS]
                if len(content) > MAX_FILE_CHARS:
                    snippet += "\n... [truncated]"
                fetched_files[path] = snippet
                total_chars += len(snippet)

    # 5. GitHub metadata relevant to the query
    if any(g in groups for g in ["deploy"]):
        deployments = _fetch(f"{GITHUB_API}/repos/{username}/{reponame}/deployments", token)
        if deployments and isinstance(deployments, list):
            dep_summary = f"Total deployments: {len(deployments)}\n"
            for d in deployments[:5]:
                dep_summary += f"  - [{d.get('environment','?')}] {d.get('created_at','')[:10]} sha:{d.get('sha','')[:7]}\n"
            context_parts.append("=== DEPLOYMENTS ===\n" + dep_summary)

    if any(g in groups for g in ["api", "auth"]):
        contributors = _fetch(f"{GITHUB_API}/repos/{username}/{reponame}/contributors", token, {"per_page": "10"})
        if contributors and isinstance(contributors, list):
            c_summary = ", ".join([c.get("login", "?") for c in contributors[:10]])
            context_parts.append(f"=== TOP CONTRIBUTORS ===\n{c_summary}\n")

    # 6. Append fetched file contents
    if fetched_files:
        files_block = "=== REPOSITORY FILE CONTENTS ===\n"
        for path, content in fetched_files.items():
            files_block += f"\n--- {path} ---\n{content}\n"
        context_parts.append(files_block)

    return "\n\n".join(context_parts)
