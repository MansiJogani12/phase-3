import asyncio
from datetime import datetime, timezone
from app.http_compat import JSONResponse
from app.utils.github_api import create_github_client, strip_git_suffix

async def fetch_repo_file_contents(username: str, reponame: str, path: str, user_id: str):
    reponame = strip_git_suffix(reponame)
    try:
        client = await create_github_client(user_id)
        response = await client.get(f"/repos/{username}/{reponame}/contents/{path}")
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except Exception as e:
        status = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        return JSONResponse(status_code=status, content={"message": "Error fetching file content from GitHub."})

async def fetch_issue_timeline(username: str, reponame: str, issue_number: str, user_id: str):
    reponame = strip_git_suffix(reponame)
    try:
        client = await create_github_client(user_id)
        response = await client.get(
            f"/repos/{username}/{reponame}/issues/{issue_number}/timeline",
            headers={"Accept": "application/vnd.github.mockingbird-preview+json"}
        )
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except Exception as e:
        status = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        return JSONResponse(status_code=status, content={"message": "Error fetching issue timeline from GitHub."})

async def fetch_repo_details(username: str, reponame: str, user_id: str):
    reponame = strip_git_suffix(reponame)
    try:
        client = await create_github_client(user_id)
        response = await client.get(f"/repos/{username}/{reponame}")
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except Exception as e:
        import traceback
        traceback.print_exc()
        status = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        return JSONResponse(status_code=status, content={"message": "Error fetching repository data from GitHub."})

async def fetch_readme(username: str, reponame: str, user_id: str):
    reponame = strip_git_suffix(reponame)
    try:
        client = await create_github_client(user_id)
        response = await client.get(f"/repos/{username}/{reponame}/readme")
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except Exception as e:
        status = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        return JSONResponse(status_code=status, content={"message": "Error fetching README from GitHub."})

async def fetch_file_commits(username: str, reponame: str, path: str, user_id: str):
    reponame = strip_git_suffix(reponame)
    if not path:
        return JSONResponse(status_code=400, content={"message": "A file path query parameter is required."})
    try:
        client = await create_github_client(user_id)
        response = await client.get(f"/repos/{username}/{reponame}/commits", params={"path": path})
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except Exception as e:
        status = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        return JSONResponse(status_code=status, content={"message": "Error fetching file commit history from GitHub."})

async def fetch_deployments(username: str, reponame: str, user_id: str):
    reponame = strip_git_suffix(reponame)
    try:
        client = await create_github_client(user_id)
        deployments_response = await client.get(f"/repos/{username}/{reponame}/deployments")
        deployments_response.raise_for_status()
        deployments = deployments_response.json()
        
        if not deployments:
            return JSONResponse(content=[])
            
        BATCH_SIZE = 5
        deployments_with_statuses = []
        
        for i in range(0, len(deployments), BATCH_SIZE):
            batch = deployments[i:i + BATCH_SIZE]
            
            async def get_status(deployment):
                try:
                    status_res = await client.get(deployment["statuses_url"])
                    status_res.raise_for_status()
                    deployment["statuses"] = status_res.json()
                except Exception:
                    deployment["statuses"] = []
                return deployment
                
            batch_results = await asyncio.gather(*(get_status(d) for d in batch))
            deployments_with_statuses.extend(batch_results)
            
        latest_deployments = {}
        for deployment in deployments_with_statuses:
            statuses = deployment.get("statuses", [])
            if statuses:
                latest_success_status = next(
                    (s for s in statuses if s.get("state") == "success"),
                    None
                )
                if latest_success_status:
                    deployment_data = {
                        "url": latest_success_status.get("environment_url") or latest_success_status.get("target_url"),
                        "environment": deployment.get("environment"),
                        "createdAt": deployment.get("created_at"),
                        "sha": deployment.get("sha"),
                        "id": deployment.get("id"),
                    }
                    environment = deployment_data["environment"] or "Other"
                    previous = latest_deployments.get(environment)
                    if not previous or deployment_data["createdAt"] > previous["createdAt"]:
                        latest_deployments[environment] = deployment_data
                        
        return JSONResponse(content=list(latest_deployments.values()))
    except Exception as e:
        status = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        if status == 404:
            return JSONResponse(content=[])
        return JSONResponse(status_code=status, content={"message": "Error fetching deployments from GitHub."})

async def fetch_git_tree(username: str, reponame: str, branch: str, user_id: str):
    reponame = strip_git_suffix(reponame)
    try:
        client = await create_github_client(user_id)
        
        if not branch or branch == "default":
            repo_res = await client.get(f"/repos/{username}/{reponame}")
            repo_res.raise_for_status()
            branch = repo_res.json().get("default_branch")
            
        branch_info = await client.get(f"/repos/{username}/{reponame}/branches/{branch}")
        branch_info.raise_for_status()
        tree_sha = branch_info.json()["commit"]["commit"]["tree"]["sha"]
        
        tree_res = await client.get(f"/repos/{username}/{reponame}/git/trees/{tree_sha}?recursive=1")
        tree_res.raise_for_status()
        
        return JSONResponse(content=tree_res.json())
    except Exception as e:
        status = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        return JSONResponse(status_code=status, content={"message": "Error fetching Git tree from GitHub."})

async def fetch_contributors(username: str, reponame: str, user_id: str):
    reponame = strip_git_suffix(reponame)
    try:
        client = await create_github_client(user_id)
        response = await client.get(f"/repos/{username}/{reponame}/contributors")
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except Exception as e:
        status = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        return JSONResponse(status_code=status, content={"message": "Error fetching contributors from GitHub."})

async def fetch_issues(username: str, reponame: str, user_id: str):
    reponame = strip_git_suffix(reponame)
    try:
        client = await create_github_client(user_id)
        open_issues_res, closed_issues_res = await asyncio.gather(
            client.get(f"/repos/{username}/{reponame}/issues", params={"state": "open", "per_page": 50}),
            client.get(f"/repos/{username}/{reponame}/issues", params={"state": "closed", "per_page": 50})
        )
        open_issues_res.raise_for_status()
        closed_issues_res.raise_for_status()
        
        issues_data = {
            "open": open_issues_res.json(),
            "closed": closed_issues_res.json()
        }
        return JSONResponse(content=issues_data)
    except Exception as e:
        status = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        return JSONResponse(status_code=status, content={"message": "Error fetching issues from GitHub."})

async def fetch_pull_requests(username: str, reponame: str, user_id: str):
    reponame = strip_git_suffix(reponame)
    try:
        client = await create_github_client(user_id)
        response = await client.get(f"/repos/{username}/{reponame}/pulls", params={
            "state": "all",
            "per_page": 100,
            "sort": "updated",
            "direction": "desc"
        })
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except Exception as e:
        status = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        return JSONResponse(status_code=status, content={"message": "Error fetching pull requests."})

async def fetch_good_first_issues(username: str, reponame: str, user_id: str):
    reponame = strip_git_suffix(reponame)
    try:
        client = await create_github_client(user_id)
        response = await client.get(f"/repos/{username}/{reponame}/issues", params={
            "labels": "good first issue,help wanted",
            "state": "open"
        })
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except Exception as e:
        status = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        return JSONResponse(status_code=status, content={"message": "Error fetching good first issues from GitHub."})

async def fetch_code_hotspots(username: str, reponame: str, user_id: str):
    reponame = strip_git_suffix(reponame)
    try:
        client = await create_github_client(user_id)
        commits_res = await client.get(f"/repos/{username}/{reponame}/commits", params={"per_page": 100})
        commits_res.raise_for_status()
        commits = commits_res.json()
        
        BATCH_SIZE = 10
        file_churn = {}
        
        for i in range(0, len(commits), BATCH_SIZE):
            batch = commits[i:i + BATCH_SIZE]
            
            async def get_commit_detail(commit):
                try:
                    res = await client.get(commit["url"])
                    res.raise_for_status()
                    return res.json()
                except Exception:
                    return None
                    
            commit_details = await asyncio.gather(*(get_commit_detail(c) for c in batch))
            
            for detail in commit_details:
                if detail and "files" in detail:
                    for file in detail["files"]:
                        filename = file.get("filename")
                        if filename:
                            file_churn[filename] = file_churn.get(filename, 0) + 1
                            
        hotspots = [{"path": path, "churn": churn} for path, churn in file_churn.items()]
        hotspots.sort(key=lambda x: x["churn"], reverse=True)
        hotspots = hotspots[:50]
        
        return JSONResponse(content=hotspots)
    except Exception as e:
        status = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        return JSONResponse(status_code=status, content={"message": "Error fetching code hotspots from GitHub."})

async def get_repo_timeline(username: str, reponame: str, user_id: str):
    reponame = strip_git_suffix(reponame)
    try:
        client = await create_github_client(user_id)
        
        branches_res = await client.get(f"/repos/{username}/{reponame}/branches")
        branches_res.raise_for_status()
        branches_data = branches_res.json()
        
        tags_res = await client.get(f"/repos/{username}/{reponame}/tags")
        tags_res.raise_for_status()
        tags_data = tags_res.json()
        
        commits = []
        page = 1
        per_page = 100
        
        while len(commits) < 500:
            commits_res = await client.get(f"/repos/{username}/{reponame}/commits", params={"per_page": per_page, "page": page})
            commits_res.raise_for_status()
            page_commits = commits_res.json()
            if not page_commits:
                break
            commits.extend(page_commits)
            if len(page_commits) < per_page:
                break
            page += 1
            
        tag_map = {tag["commit"]["sha"]: tag["name"] for tag in tags_data}
        
        processed_commits = []
        for commit in commits:
            author_login = commit.get("author", {}).get("login") if commit.get("author") else commit.get("commit", {}).get("author", {}).get("name")
            author_avatar = commit.get("author", {}).get("avatar_url") if commit.get("author") else None
            processed_commits.append({
                "sha": commit.get("sha"),
                "message": commit.get("commit", {}).get("message"),
                "author": {
                    "name": commit.get("commit", {}).get("author", {}).get("name"),
                    "login": author_login,
                    "avatar_url": author_avatar
                },
                "date": commit.get("commit", {}).get("author", {}).get("date"),
                "parents": [p.get("sha") for p in commit.get("parents", [])],
                "tag": tag_map.get(commit.get("sha"))
            })
            
        response_payload = {
            "commits": processed_commits,
            "branches": [{"name": b.get("name"), "sha": b.get("commit", {}).get("sha")} for b in branches_data],
            "tags": [{"name": t.get("name"), "sha": t.get("commit", {}).get("sha")} for t in tags_data]
        }
        
        return JSONResponse(content=response_payload)
    except Exception as e:
        status = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        return JSONResponse(status_code=status, content={"message": "Failed to fetch repository timeline data from GitHub."})

def date_from_iso(iso_str):
    if not iso_str:
        return datetime.now(timezone.utc)
    return datetime.fromisoformat(iso_str.replace('Z', '+00:00'))

async def fetch_repo_insights(username: str, reponame: str, user_id: str):
    reponame = strip_git_suffix(reponame)
    try:
        client = await create_github_client(user_id)
        prs_res = await client.get(f"/repos/{username}/{reponame}/pulls", params={"state": "closed", "per_page": 100})
        prs_res.raise_for_status()
        prs_data = prs_res.json()
        
        merged_prs = [pr for pr in prs_data if pr.get("merged_at")]
        
        total_ms = 0
        for pr in merged_prs:
            created_at = date_from_iso(pr.get("created_at"))
            merged_at = date_from_iso(pr.get("merged_at"))
            total_ms += (merged_at - created_at).total_seconds() * 1000
            
        average_merge_time = (total_ms / len(merged_prs)) if merged_prs else None
        acceptance_rate = round((len(merged_prs) / len(prs_data)) * 100) if prs_data else 0
        
        return JSONResponse(content={
            "averageMergeTime": average_merge_time,
            "acceptanceRate": acceptance_rate,
            "totalClosed": len(prs_data),
            "mergedCount": len(merged_prs)
        })
    except Exception as e:
        status = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        return JSONResponse(status_code=status, content={"message": "Error fetching pull request insights from GitHub."})
