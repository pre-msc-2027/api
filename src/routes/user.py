from fastapi import APIRouter, Depends, HTTPException
from src.services.github_service import get_user_info, get_user_repos
from src.dependencies.auth import get_access_token

router = APIRouter()

@router.get("/user/info")
async def user_info(token: str = Depends(get_access_token)):
    return await get_user_info(token)

@router.get("/user/repos")
async def user_repos(token: str = Depends(get_access_token)):
    return await get_user_repos(token) 