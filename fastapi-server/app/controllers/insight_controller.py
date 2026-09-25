import asyncio
import httpx
import base64
import json
import re
from app.http_compat import JSONResponse
from app.utils.github_api import create_github_client

async def fetch_and_merge_dependencies(client, owner: str, repo: str, package_nodes: list):
    all_dependencies = {}
    
    async def fetch_file(node):
        try:
            res = await client.get(f"/repos/{owner}/{repo}/contents/{node['path']}")
            res.raise_for_status()
            data = res.json()
            content_str = base64.b64decode(data['content']).decode('utf-8')
            content = json.loads(content_str)
            deps = content.get('dependencies', {})
            dev_deps = content.get('devDependencies', {})
            return {**deps, **dev_deps}
        except Exception as e:
            print(f"Could not read {node['path']} in {owner}/{repo}: {e}")
            return {}
            
    tasks = [fetch_file(node) for node in package_nodes]
    results = await asyncio.gather(*tasks)
    
    for deps in results:
        all_dependencies.update(deps)
        
    return all_dependencies


async def check_osv_vulnerabilities(dependencies_obj: dict):
    if not dependencies_obj:
        return []
        
    queries = []
    for name, version in dependencies_obj.items():
        clean_version = re.sub(r'[\^~>=<]', '', version)
        queries.append({
            "package": {"name": name, "ecosystem": "npm"},
            "version": clean_version
        })
        
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post('https://api.osv.dev/v1/querybatch', json={"queries": queries})
            response.raise_for_status()
            results = response.json().get('results', [])
            
            vulnerable_packages = []
            for i, res in enumerate(results):
                vulns = res.get('vulns')
                if vulns and len(vulns) > 0:
                    vulnerabilities = []
                    for v in vulns:
                        vulnerabilities.append({
                            "id": v.get("id"),
                            "summary": v.get("summary", "No summary available."),
                            "severity": v.get("database_specific", {}).get("severity", "UNKNOWN") if v.get("database_specific") else "UNKNOWN",
                            "details": v.get("details", "")
                        })
                    vulnerable_packages.append({
                        "package": queries[i]["package"]["name"],
                        "version": queries[i]["version"],
                        "vulnerabilities": vulnerabilities
                    })
            return vulnerable_packages
    except Exception as e:
        print(f"OSV API Error: {e}")
        raise Exception("Failed to fetch vulnerability data from OSV.")


async def scan_single_repo_vulnerabilities(username: str, reponame: str, user_id: str):
    try:
        client = await create_github_client(user_id)
        
        repo_details_res = await client.get(f"/repos/{username}/{reponame}")
        repo_details_res.raise_for_status()
        default_branch = repo_details_res.json().get("default_branch")
        
        tree_res = await client.get(f"/repos/{username}/{reponame}/git/trees/{default_branch}?recursive=1")
        tree_res.raise_for_status()
        
        tree = tree_res.json().get("tree", [])
        
        package_nodes = [
            node for node in tree 
            if node.get("type") == "blob" and node.get("path", "").endswith("package.json") and "node_modules/" not in node.get("path", "")
        ]
        package_nodes.sort(key=lambda x: len(x.get("path", "").split("/")))
        package_nodes = package_nodes[:5]
        
        if not package_nodes:
            return JSONResponse(content={"message": "No package.json found", "vulnerabilities": []})
            
        all_dependencies = await fetch_and_merge_dependencies(client, username, reponame, package_nodes)
        
        if not all_dependencies:
            return JSONResponse(content={"message": "No dependencies found to scan", "vulnerabilities": []})
            
        vulnerabilities = await check_osv_vulnerabilities(all_dependencies)
        
        return JSONResponse(content={"repository": f"{username}/{reponame}", "vulnerabilities": vulnerabilities})
        
    except Exception as e:
        print(f"Error scanning {username}/{reponame}: {e}")
        return JSONResponse(status_code=500, content={"error": "Failed to scan repository for vulnerabilities."})


async def scan_all_repos_vulnerabilities(user_id: str):
    try:
        client = await create_github_client(user_id)
        repos_res = await client.get("/user/repos?per_page=100&affiliation=owner")
        repos_res.raise_for_status()
        repos = repos_res.json()
        
        scan_results = {}
        BATCH_SIZE = 20
        
        for i in range(0, len(repos), BATCH_SIZE):
            batch = repos[i:i + BATCH_SIZE]
            
            async def scan_repo(repo):
                try:
                    default_branch = repo.get("default_branch")
                    owner_login = repo.get("owner", {}).get("login")
                    repo_name = repo.get("name")
                    
                    tree_res = await client.get(f"/repos/{owner_login}/{repo_name}/git/trees/{default_branch}?recursive=1")
                    tree_res.raise_for_status()
                    tree = tree_res.json().get("tree", [])
                    
                    package_nodes = [
                        node for node in tree 
                        if node.get("type") == "blob" and node.get("path", "").endswith("package.json") and "node_modules/" not in node.get("path", "")
                    ]
                    package_nodes.sort(key=lambda x: len(x.get("path", "").split("/")))
                    package_nodes = package_nodes[:5]
                    
                    if not package_nodes:
                        return
                        
                    all_dependencies = await fetch_and_merge_dependencies(client, owner_login, repo_name, package_nodes)
                    
                    if not all_dependencies:
                        return
                        
                    vulns = await check_osv_vulnerabilities(all_dependencies)
                    if vulns:
                        scan_results[repo_name] = vulns
                except Exception as err:
                    print(f"Skipping {repo.get('name')} due to error: {err}")
                    
            await asyncio.gather(*(scan_repo(repo) for repo in batch))
            
        return JSONResponse(content={"totalReposScanned": len(repos), "vulnerableRepos": scan_results})
        
    except Exception as e:
        print(f"Bulk scan error: {e}")
        return JSONResponse(status_code=500, content={"error": "Failed to complete bulk vulnerability scan."})


async def fetch_dependency_health(username: str, reponame: str, user_id: str):
    try:
        client = await create_github_client(user_id)
        
        repo_details_res = await client.get(f"/repos/{username}/{reponame}")
        repo_details_res.raise_for_status()
        default_branch = repo_details_res.json().get("default_branch")
        
        tree_res = await client.get(f"/repos/{username}/{reponame}/git/trees/{default_branch}?recursive=1")
        tree_res.raise_for_status()
        tree = tree_res.json().get("tree", [])
        
        package_nodes = [
            node for node in tree 
            if node.get("type") == "blob" and node.get("path", "").endswith("package.json") and "node_modules/" not in node.get("path", "")
        ]
        package_nodes.sort(key=lambda x: len(x.get("path", "").split("/")))
        package_nodes = package_nodes[:5]
        
        if not package_nodes:
            return JSONResponse(content={"error": "package.json not found in this repository."})
            
        all_dependencies = await fetch_and_merge_dependencies(client, username, reponame, package_nodes)
        
        if not all_dependencies:
            return JSONResponse(content={"dependencies": [], "summary": {"total": 0, "outdated": 0, "deprecated": 0, "licenses": []}})
            
        dependency_entries = list(all_dependencies.items())
        health_report = []
        BATCH_SIZE = 5
        
        async with httpx.AsyncClient(timeout=30.0) as npm_client:
            for i in range(0, len(dependency_entries), BATCH_SIZE):
                batch = dependency_entries[i:i + BATCH_SIZE]
                
                async def check_npm(name, version):
                    try:
                        res = await npm_client.get(f"https://registry.npmjs.org/{name}")
                        res.raise_for_status()
                        data = res.json()
                        latest_version = data.get("dist-tags", {}).get("latest")
                        license_val = data.get("license", "N/A")
                        if isinstance(license_val, dict):
                            license = license_val.get("type", "N/A")
                        else:
                            license = str(license_val)
                        is_deprecated = bool(data.get("deprecated"))
                        clean_version = re.sub(r'[\^~>=<]', '', version)
                        is_outdated = latest_version != clean_version
                        
                        return {
                            "name": name,
                            "version": version,
                            "latestVersion": latest_version,
                            "license": license,
                            "isOutdated": is_outdated,
                            "isDeprecated": is_deprecated
                        }
                    except Exception as err:
                        print(f"Error fetching data for {name}: {err}")
                        return {"name": name, "version": version, "error": "Package not found in npm registry"}
                        
                batch_results = await asyncio.gather(*(check_npm(n, v) for n, v in batch))
                health_report.extend(batch_results)
                
        licenses = sorted(list(set(d.get("license") for d in health_report if d.get("license"))))
        
        summary = {
            "total": len(health_report),
            "outdated": len([d for d in health_report if d.get("isOutdated") and not d.get("error")]),
            "deprecated": len([d for d in health_report if d.get("isDeprecated") and not d.get("error")]),
            "licenses": licenses
        }
        
        final_report = {"dependencies": health_report, "summary": summary}
        return JSONResponse(content=final_report)
        
    except Exception as e:
        print(f"Error fetching dependency health: {e}")
        status_code = getattr(e.response, "status_code", 500) if hasattr(e, "response") else 500
        return JSONResponse(status_code=status_code, content={"message": "Error fetching dependency health."})
