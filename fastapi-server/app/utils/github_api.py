import httpx
from bson.objectid import ObjectId
from app.database import get_db

async def get_github_token(user_id: str = None) -> str:
    if user_id:
        db = get_db()
        user = db["users"].find_one({"_id": ObjectId(user_id)})
        if user and user.get("githubAccessToken"):
            return user["githubAccessToken"]
    return None

class GitHubClientWrapper:
    def __init__(self, token: str):
        self.token = token
        self.base_headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.base_headers["Authorization"] = f"token {self.token}"

    async def get(self, url, **kwargs):
        headers = kwargs.pop("headers", {})
        headers.update(self.base_headers)
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://api.github.com" + url
        elif url.startswith("https://api.github.comhttps://api.github.com"):
            url = url.replace("https://api.github.comhttps://api.github.com", "https://api.github.com")
        async with httpx.AsyncClient(timeout=30.0) as client:
            return await client.get(url, headers=headers, **kwargs)

async def create_github_client(user_id: str = None) -> GitHubClientWrapper:
    token = await get_github_token(user_id)
    return GitHubClientWrapper(token)

def strip_git_suffix(name: str) -> str:
    if name and name.lower().endswith(".git"):
        return name[:-4]
    return name
