from src.repositories.scans import ScansRepository
from src.generics import Service
from src.exceptions import not_found
from src.schemas.scan import ScanCreate, ScanOut, ScanOptionsSchema
from src import models
from typing import List
from utils.counter import get_next_sequence


class ScansService(Service):

    def __init__(self):
        self.scans_repository= ScansRepository()

    async def get_scan(self, scan_id: str) -> ScanOut:
        scan = await self.scans_repository.get_scan_by_id(scan_id)
        if scan is None:
            raise not_found.ObjectNotFoundError("scan", "scan_id", str(scan_id))
        return ScanOut.model_validate(scan)
    
    async def get_scan_options(self, scan_id: str) -> ScanOptionsSchema:
        scan = await self.scans_repository.get_scan_by_id(scan_id)
        if scan is None:
            raise not_found.ObjectNotFoundError("scan", "scan_id", scan_id)
        return ScanOptionsSchema.model_validate(scan.scan_options)

    async def create_scan(self, scan_create: ScanCreate) -> ScanOut:
        scan_id = await get_next_sequence("scan_id")

        scan_model = models.Scan(
        scan_id=scan_id,
        scan_options=scan_create.scan_options
        )

        await scan_model.insert()
        return ScanOut.model_validate(scan_model)

    async def get_scans(self, repo_url: str) -> List[int]:
        scans = await self.scans_repository.get_by_repo_name(repo_url)
        return [scan.scan_id for scan in scans]