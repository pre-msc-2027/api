from src.generics import Repository
from typing import Optional, List
from src import models

class ScansRepository(Repository):

    def __init__(self):
        super().__init__(models.Scan)

    async def get_scan_by_id(self, scan_id: str) -> Optional[models.Scan]:
        return await models.Scan.find_one(models.Scan.scan_id == scan_id)

    async def create(self, scan: models.Scan) -> models.Scan:
        await scan.insert()
        return scan

    async def get_by_repo_url(self, repo_url: str) -> List[models.Scan]:
        return await self.model.find(
            {"scan_options.repo_url": repo_url}
        ).to_list()