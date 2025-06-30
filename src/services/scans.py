from src.repositories.scans import ScansRepository
from src.generics import Service
from src.exceptions import not_found
from src.schemas.scan import ScanCreate, ScanOut
from src import models
from beanie import PydanticObjectId
from typing import List
from utils.counter import get_next_sequence


class ScansService(Service):

    def __init__(self):
        self.scans_repository= ScansRepository()

    async def get_scan(self, scan_id: PydanticObjectId) -> ScanOut:
        scan = await self.scans_repository.get_scan_by_id(scan_id)
        if scan is None:
            raise not_found.ObjectNotFoundError("scan", "scan_id", str(scan_id))
        return ScanOut.model_validate(scan)

    async def create_scan(self, scan_create: ScanCreate) -> ScanOut:
        
        scan_id = await get_next_sequence("scan_id")
        scan_model = models.Scan(scan_id=scan_id, **scan_create.model_dump())
        created = await self.scans_repository.create(scan_model)
        return ScanOut.model_validate(created)

    async def get_scans(self) -> List[PydanticObjectId]:
        return await self.scans_repository.get_all()