import httpx

GITHUB_API = "https://api.github.com"

async def get_user_info(access_token: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{GITHUB_API}/user",
            headers={'Authorization': f'token {access_token}', 'Accept': "application/vnd.github.v3+json"}
        )

        if resp.status_code != 200:
            raise httpx.HTTPStatusError(f"Failed to fetch user info: {resp.status_code}", request=resp.request, response=resp)

    return resp.json()

async def get_user_repos(access_token: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{GITHUB_API}/user/repos",
            headers={'Authorization': f'token {access_token}', 'Accept': "application/vnd.github.v3+json"}
        )
        if resp.status_code != 200:
            raise httpx.HTTPStatusError(f"Failed to fetch user repositories: {resp.status_code}", request=resp.request, response=resp)
    return resp.json()

async def get_repo_files(access_token: str, owner: str, repo: str, branch: str = "main"):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/contents",
            params={"ref": branch},
            headers={'Authorization': f'token {access_token}', 'Accept': "application/vnd.github.v3+json"}
        )
        if resp.status_code != 200:
            raise httpx.HTTPStatusError(f"Failed to fetch repository files: {resp.status_code}", request=resp.request, response=resp)
    return resp.json()
