from generics import Repository
from beanie import PydanticObjectId
from typing import Optional, List
from src import models

class ScansRepository(Repository):

    def __init__(self):
        super().__init__(models.Scan)

    async def get_scan_by_id(self, scan_id: PydanticObjectId) -> Optional[models.Scan]:
        return await models.Scan.get(scan_id)

    async def create(self, scan: models.Scan) -> models.Scan:
        await scan.insert()
        return scan

    async def get_all(self) -> List[PydanticObjectId]:
        scans = await models.Scan.find_all().to_list()
        return [scan.id for scan in scans]