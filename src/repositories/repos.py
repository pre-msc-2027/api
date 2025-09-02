from typing import Optional
from src.models.repo import Repo
from src.generics import Repository

class ReposRepository(Repository):
    def __init__(self):
        super().__init__(Repo)

    async def get_by_url(self, repo_url: str) -> Optional[Repo]:
        return await self.model.find_one({'repo_url': repo_url})

    async def get_all_by_name(self, name: str):
        return await Repo.find({'user.name': name}).to_list()
