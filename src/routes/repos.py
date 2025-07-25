from fastapi import APIRouter, Depends
from typing import List
from src.schemas.repo import RepoCreate, RepoOut
from src.services.repos import ReposService
from src.exceptions import not_found

router = APIRouter(prefix="/repositories", tags=["repositories"])

@router.get("/user/{user}", response_model=List[RepoOut])
async def list_repositories(user: str, service: ReposService = Depends(ReposService)):
    return await service.get_all(user)

@router.post("/", response_model=RepoOut, status_code=201)
async def create_repository(repo: RepoCreate, service: ReposService = Depends(ReposService)):
    return await service.create(repo)

@router.get("/{repo_url}", response_model=RepoOut)
async def get_repository(repo_url: str, service: ReposService = Depends(ReposService)):
    try:
        return await service.get_by_url(repo_url)
    except not_found.ObjectNotFoundError as e:
        raise e.get_response()