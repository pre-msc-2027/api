from fastapi import APIRouter, Depends, HTTPException
from src.services.github_service import get_user_info, get_user_repos

router = APIRouter()

def get_access_token(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Format d'Authorization incorrect")
    token = authorization.split(" ", 1)[1]
    if not token:
        raise HTTPException(status_code=401, detail="Access token manquant")
    return token

@router.get("/info")
async def user_info(token: str = Depends(get_access_token)):
    return await get_user_info(token)

@router.get("/repos")
async def user_repos(token: str = Depends(get_access_token)):
    return await get_user_repos(token)