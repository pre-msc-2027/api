from fastapi import APIRouter, Depends
from typing import List
from src.schemas import ScanCreate, ScanOut, ScanOptionsSchema, AnalysisSchema, AnalysisWithRulesResponse, LogEntrySchema, RepoSummary, AICommentSchema
from src.services import ScansService
from src.exceptions import not_found

router = APIRouter(prefix="/scans", tags=["scans"])

@router.get("/summary/{name}", response_model=List[RepoSummary])
async def get_user_repo_summary(name: str, service: ScansService = Depends(ScansService)):
    return await service.get_user_repo_summaries(name)

@router.get("/{scan_id}", response_model=ScanOut)
async def get_scan(scan_id: str, service: ScansService = Depends(ScansService)):
    try:
        return await service.get_scan(scan_id)
    except not_found.ObjectNotFoundError as e:
        raise e.get_response()
    
@router.get("/options/{scan_id}", response_model=ScanOptionsSchema)
async def get_scan_option(scan_id: str, service: ScansService = Depends(ScansService)):
    try:
        return await service.get_scan_options(scan_id)
    except not_found.ObjectNotFoundError as e:
        raise e.get_response()

@router.post("/", response_model=ScanOut, status_code=201)
async def create_scan(scan: ScanCreate, service: ScansService = Depends(ScansService)):
    return await service.create_scan(scan)

@router.post("/logs/{scan_id}", response_model=ScanOut, status_code=201)
async def fill_analysis(scan_id: str, logs: LogEntrySchema, service: ScansService = Depends(ScansService)):
    print("📥 Received logs:", logs.model_dump())
    return await service.fill_logs(scan_id, logs)

@router.post("/ai_comment/{scan_id}", response_model=ScanOut, status_code=201)
async def fill_analysis(scan_id: str, ai_comments: List[AICommentSchema], service: ScansService = Depends(ScansService)):
    return await service.fill_ai_comment(scan_id, ai_comments)

@router.post("/analyse/{scan_id}", response_model=ScanOut, status_code=201)
async def fill_analysis(scan_id: str, scan: AnalysisSchema, service: ScansService = Depends(ScansService)):
    return await service.fill_analysis(scan_id, scan)

@router.get("/analyse_with_rules/{scan_id}", response_model=AnalysisWithRulesResponse)
async def get_analysis_with_rules(scan_id: str, service: ScansService = Depends(ScansService)):
    try:
        return await service.get_analysis_with_rules(scan_id)
    except not_found.ObjectNotFoundError as e:
        raise e.get_response()
    
@router.get("/analyse/{scan_id}", response_model=AnalysisSchema)
async def get_analysis(scan_id: str, service: ScansService = Depends(ScansService)):
    try:
        return await service.get_analysis(scan_id)
    except not_found.ObjectNotFoundError as e:
        raise e.get_response()