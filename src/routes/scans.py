from fastapi import APIRouter, Depends
from typing import List
from src.schemas import ScanCreate, ScanOut, ScanOptionsSchema
from src.services import ScansService
from src.exceptions import not_found

router = APIRouter(prefix="/scans", tags=["scans"])

@router.get("/repo/{repo_url}", response_model=List[ScanOut])
async def get_scans(repo_url: str, service: ScansService = Depends(ScansService)):
    scan_ids = await service.get_scans()
    scans = [await service.get_scan(rid) for rid in scan_ids]
    return scans


@router.get("/{scan_id}", response_model=ScanOut)
async def get_scan(scan_id: int, service: ScansService = Depends(ScansService)):
    try:
        return await service.get_scan(scan_id)
    except not_found.ObjectNotFoundError as e:
        raise e.get_response()
    
@router.get("/options/{scan_id}", response_model=ScanOptionsSchema)
async def get_scan_option(scan_id: int, service: ScansService = Depends(ScansService)):
    try:
        return await service.get_scan_options(scan_id)
    except not_found.ObjectNotFoundError as e:
        raise e.get_response()

@router.post("/", response_model=ScanOut, status_code=201)
async def create_scan(scan: ScanCreate, service: ScansService = Depends(ScansService)):
    return await service.create_scan(scan)