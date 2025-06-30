from repositories.scans import ScansRepository
from src.generics import Service
from src.repositories import ScansRepository
from src.exceptions import not_found
from src.schemas.scan import ScanCreate, ScanOut
from src import models
from beanie import PydanticObjectId
from typing import List


class ScansService(Service):

    scans_repository: ScansRepository

    def __init__(self):
        scans_repository= ScansRepository()

    async def get_scan(self, scan_id: PydanticObjectId) -> ScanOut:
        scan = await self.scans_repository.get_scan_by_id(scan_id)
        if scan is None:
            raise not_found.ObjectNotFoundError("scan", "scan_id", str(scan_id))
        return ScanOut.model_validate(scan)

    async def create_scan(self, scan_create: ScanCreate) -> ScanOut:
        
        scan_model = models.scan(**scan_create.model_dump())
        created = await self.scans_repository.create(scan_model)
        return ScanOut.model_validate(created)

    async def get_scans(self) -> List[PydanticObjectId]:
        return await self.scans_repository.get_all()