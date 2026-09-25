from flask import Blueprint, request
from app.middlewares.auth_middleware import require_auth
from app.controllers.github_controller import (
    fetch_repo_file_contents, fetch_issue_timeline, fetch_repo_details,
    fetch_readme, fetch_file_commits, fetch_deployments, fetch_git_tree,
    fetch_contributors, fetch_issues, fetch_pull_requests,
    fetch_good_first_issues, fetch_code_hotspots, get_repo_timeline,
    fetch_repo_insights,
)
from app.controllers.insight_controller import (
    fetch_dependency_health, scan_all_repos_vulnerabilities,
    scan_single_repo_vulnerabilities,
)
from app.controllers.chat_controller import chat_with_repo

repo_bp = Blueprint('repo', __name__)


@repo_bp.get('/<username>/<reponame>/file/<path:path>')
async def fetch_repo_file_contents_route(username, reponame, path):
    return await fetch_repo_file_contents(username, reponame, path, await require_auth())


@repo_bp.get('/repos/<username>/<reponame>/file/<path:path>')
async def fetch_repo_file_contents_compat_route(username, reponame, path):
    return await fetch_repo_file_contents(username, reponame, path, await require_auth())


@repo_bp.get('/<username>/<reponame>/issues/<issue_number>/timeline')
async def fetch_issue_timeline_route(username, reponame, issue_number):
    return await fetch_issue_timeline(username, reponame, issue_number, await require_auth())


@repo_bp.get('/<username>/<reponame>/insights/dependencies')
async def fetch_dependency_health_route(username, reponame):
    return await fetch_dependency_health(username, reponame, await require_auth())


@repo_bp.get('/<username>/<reponame>')
async def fetch_repo_details_route(username, reponame):
    return await fetch_repo_details(username, reponame, await require_auth())


@repo_bp.get('/<username>/<reponame>/readme')
async def fetch_readme_route(username, reponame):
    return await fetch_readme(username, reponame, await require_auth())


@repo_bp.get('/<username>/<reponame>/commits')
async def fetch_file_commits_route(username, reponame):
    return await fetch_file_commits(username, reponame, request.args.get('path'), await require_auth())


@repo_bp.get('/<username>/<reponame>/deployments')
async def fetch_deployments_route(username, reponame):
    return await fetch_deployments(username, reponame, await require_auth())


@repo_bp.get('/<username>/<reponame>/git/trees/<branch>')
async def fetch_git_tree_route(username, reponame, branch):
    return await fetch_git_tree(username, reponame, branch, await require_auth())


@repo_bp.get('/<username>/<reponame>/contributors')
async def fetch_contributors_route(username, reponame):
    return await fetch_contributors(username, reponame, await require_auth())


@repo_bp.get('/<username>/<reponame>/issues')
async def fetch_issues_route(username, reponame):
    return await fetch_issues(username, reponame, await require_auth())


@repo_bp.get('/<username>/<reponame>/pulls')
async def fetch_pull_requests_route(username, reponame):
    return await fetch_pull_requests(username, reponame, await require_auth())


@repo_bp.get('/<username>/<reponame>/good-first-issues')
async def fetch_good_first_issues_route(username, reponame):
    return await fetch_good_first_issues(username, reponame, await require_auth())


@repo_bp.get('/<username>/<reponame>/hotspots')
async def fetch_code_hotspots_route(username, reponame):
    return await fetch_code_hotspots(username, reponame, await require_auth())


@repo_bp.get('/<username>/<reponame>/timeline')
async def get_repo_timeline_route(username, reponame):
    return await get_repo_timeline(username, reponame, await require_auth())


@repo_bp.get('/<username>/<reponame>/insights')
async def fetch_repo_insights_route(username, reponame):
    return await fetch_repo_insights(username, reponame, await require_auth())


@repo_bp.post('/scan/all')
async def scan_all_repos_vulnerabilities_route():
    return await scan_all_repos_vulnerabilities(await require_auth())


@repo_bp.post('/scan/<username>/<reponame>')
async def scan_single_repo_vulnerabilities_route(username, reponame):
    return await scan_single_repo_vulnerabilities(username, reponame, await require_auth())


@repo_bp.post('/<username>/<reponame>/chat')
async def chat_with_repo_route(username, reponame):
    return await chat_with_repo(username, reponame)
