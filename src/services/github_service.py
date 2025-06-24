import httpx

GITHUB_API = "https://api.github.com"

async def get_user_info(access_token: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{GITHUB_API}/user",
            headers={'Authorization': f'token {access_token}', 'Accept': "application/vnd.github.v3+json"}
        )
    return resp.json()

async def get_user_repos(access_token: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{GITHUB_API}/user/repos",
            headers={'Authorization': f'token {access_token}', 'Accept': "application/vnd.github.v3+json"}
        )
    return resp.json()

async def get_repo_files(access_token: str, owner: str, repo: str, branch: str = "main"):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/contents",
            params={"ref": branch},
            headers={'Authorization': f'token {access_token}', 'Accept': "application/vnd.github.v3+json"}
        )
    return resp.json()
