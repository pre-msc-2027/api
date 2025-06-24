from fastapi import APIRouter, Depends, HTTPException
from src.services.github_service import get_repo_files

router = APIRouter()

def get_access_token(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Format d'Authorization incorrect")
    token = authorization.split(" ", 1)[1]
    if not token:
        raise HTTPException(status_code=401, detail="Access token manquant")
    return token

@router.get("/{owner}/{repo}/files")
async def repo_files(owner: str, repo: str, branch: str = "main", token: str = Depends(get_access_token)):
    return await get_repo_files(token, owner, repo, branch)
