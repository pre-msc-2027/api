from typing import List
from src.repositories.repos import ReposRepository
from src.schemas.repo import RepoCreate, RepoOut
from src import models
from src.exceptions import not_found

class ReposService:
    def __init__(self):
        self.repositories_repos = ReposRepository()

    async def get_all(self, name: str) -> List[RepoOut]:
        repos = await self.repositories_repos.get_all_by_name(name)
        return [RepoOut.model_validate(r.model_dump()) for r in repos]

    async def create(self, repo: RepoCreate) -> RepoOut:
        repo_model = models.Repo(**repo.model_dump())
        await repo_model.insert()
        return RepoOut.model_validate(repo_model.model_dump())

    async def get_by_url(self, repo_url: str) -> RepoOut:
        repo = await self.repositories_repos.get_by_url(repo_url)
        if repo is None:
            raise not_found.ObjectNotFoundError("repository", "repo_url", repo_url)
        return RepoOut.model_validate(repo.model_dump())
