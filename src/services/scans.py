from src.repositories.scans import ScansRepository
from src.generics import Service
from src.exceptions import not_found
from src.schemas.scan import ScanCreate, ScanOut, ScanOptionsSchema, AnalysisSchema, LogEntrySchema, AnalysisSummaryItem, RepoSummary
from src.schemas.rule import RuleOut
from src import models
from typing import List
from utils.counter import get_next_sequence
import asyncio
from utils.javaLauncher import run_java_process
from src.services.rules import RulesService
from src.schemas.ai import AnalysisWithRulesResponse


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

        asyncio.create_task(run_java_process(scan_id))
        return ScanOut.model_validate(scan_model)

    async def get_user_repo_summaries(self, user: str) -> List[RepoSummary]:
        repos = await self.repos_repository.get_all_by_user(user)
        summaries = []

        for repo in repos:
            scans = await self.scans_repository.get_all_by_repo_url(repo.repo_url)
            analyses = [
                AnalysisSummaryItem(
                    scan_id=scan.scan_id,
                    project_name=scan.project_name,
                    branch_id=scan.scan_options.branch_id
                )
                for scan in scans
            ]
            summaries.append(RepoSummary(repo_url=repo.repo_url, analyses=analyses))

        return summaries


    async def fill_analysis(self, scan_id: str, analysis: AnalysisSchema) -> ScanOut:
        scan = await self.scans_repository.get_by_scan_id(scan_id)
        if scan is None:
            raise not_found.ObjectNotFoundError("scan", "scan_id", scan_id)

        scan.analysis = analysis
        await scan.save()

        return ScanOut.model_validate(scan)
    
    async def fill_logs(self, scan_id: str, log: LogEntrySchema) -> ScanOut:
        scan = await self.scans_repository.get_by_scan_id(scan_id)
        if scan is None:
            raise not_found.ObjectNotFoundError("scan", "scan_id", scan_id)

        if scan.logs is None:
            scan.logs = []

        scan.logs.append(log)
        await scan.save()

        return ScanOut.model_validate(scan)
    
    async def get_analysis_with_rules(self, scan_id: str) -> AnalysisWithRulesResponse:
        scan = await self.scans_repository.get_by_scan_id(scan_id)
        if not scan:
            raise not_found.ObjectNotFoundError("scan", "scan_id", scan_id)
        
        if not scan.analysis or not scan.analysis.warnings:
            return AnalysisWithRulesResponse(
                analysis=AnalysisSchema.model_validate(scan.analysis),
                rules=[]
            )

        rules_ids = list({w["rules_id"] for w in scan.analysis["warnings"] if "rules_id" in w})

        rules_service = RulesService()
        rules = await rules_service.get_rules_by_ids(rules_ids)

        return AnalysisWithRulesResponse(
            analysis=AnalysisSchema.model_validate(scan.analysis),
            rules=[RuleOut.model_validate(r) for r in rules]
        )