from fastapi import APIRouter, Depends, HTTPException
from src.services.github_service import get_repo_files
from src.dependencies.auth import get_access_token

router = APIRouter()

@router.get("/{owner}/{repo}/files")
async def repo_files(owner: str, repo: str, branch: str = "main", token: str = Depends(get_access_token)):
    return await get_repo_files(token, owner, repo, branch)
