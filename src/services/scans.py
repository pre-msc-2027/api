import hashlib
from datetime import datetime

from beanie.odm.operators.update.general import Inc

from src.models.counter import Counter
from src.models.scan import ScanOptions
from src.repositories.scans import ScansRepository
from src.repositories.repos import ReposRepository
from src.generics import Service
from src.exceptions import not_found
from src.schemas.scan import ScanCreate, ScanOut, ScanOptionsSchema, AnalysisSchema, LogEntrySchema, AnalysisSummaryItem, RepoSummary, AICommentSchema
from src.schemas.rule import RuleOut
from src import models
from typing import List
from src.utils.counter import get_next_sequence
import asyncio
from src.utils.javaLauncher import run_java_process
from src.services.rules import RulesService
from src.schemas.ai import AnalysisWithRulesResponse


class ScansService(Service):

    def __init__(self):
        self.scans_repository= ScansRepository()
        self.repos_repository= ReposRepository()

    async def get_scan(self, scan_id: str) -> ScanOut:
        scan = await self.scans_repository.get_scan_by_id(scan_id)
        if scan is None:
            raise not_found.ObjectNotFoundError("scan", "scan_id", str(scan_id))
        return ScanOut.model_validate(scan.model_dump())
    
    async def get_scan_options(self, scan_id: str) -> ScanOptionsSchema:
        scan = await self.scans_repository.get_scan_by_id(scan_id)
        if scan is None:
            raise not_found.ObjectNotFoundError("scan", "scan_id", scan_id)
        return ScanOptionsSchema.model_validate(scan.scan_options.model_dump())

    async def create_scan(self, scan_create: ScanCreate) -> ScanOut:
        scan_id = await get_next_sequence("scan_id")

        scan_model = models.Scan(

        scan_id=scan_id,
        timestamp=datetime.now(),
        project_name=scan_create.project_name,
        scanned_by=scan_create.scanned_by,
        scan_version="1.1.1",
        scan_options=ScanOptions.model_validate(scan_create.scan_options.model_dump())

        )

        await scan_model.insert()

        asyncio.create_task(run_java_process(scan_id, scan_create.token))
        return ScanOut.model_validate(scan_model.model_dump())

    async def get_user_repo_summaries(self, name: str) -> List[RepoSummary]:
        repos = await self.repos_repository.get_all_by_name(name)
        print(repos)
        summaries = []

        for repo in repos:
            scans = await self.scans_repository.get_by_repo_url(repo.repo_url)
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

    async def get_next_sequence(self,key: str) -> str:
        counter = await Counter.find_one({"key": key})

        if counter:
            counter = await Counter.find_one_and_update(
                Counter.key == key,
                Inc({Counter.counter: 1}),
                return_document=True
            )
        else:
            counter = Counter(key=key, counter=1)
            await counter.insert()

        raw_value = f"{key}:{counter.counter}"
        hashed = hashlib.sha256(raw_value.encode()).hexdigest()

        return hashed

    async def fill_analysis(self, scan_id: str, analysis: AnalysisSchema) -> ScanOut:
        scan = await self.scans_repository.get_scan_by_id(scan_id)
        if scan is None:
            raise not_found.ObjectNotFoundError("scan", "scan_id", scan_id)

        scan.analysis = analysis
        await scan.save()

        return ScanOut.model_validate(scan.model_dump())
    
    async def fill_logs(self, scan_id: str, log: LogEntrySchema) -> ScanOut:
        scan = await self.scans_repository.get_scan_by_id(scan_id)
        if scan is None:
            raise not_found.ObjectNotFoundError("scan", "scan_id", scan_id)

        if scan.logs is None:
            scan.logs = []

        scan.logs.append(log)
        await scan.save()

        return ScanOut.model_validate(scan.model_dump())
    
    async def fill_ai_comment(self, scan_id: str, ai_comment: AICommentSchema) -> ScanOut:
        scan = await self.scans_repository.get_scan_by_id(scan_id)
        if scan is None:
            raise not_found.ObjectNotFoundError("scan", "scan_id", scan_id)

        if scan.ai_comments is None:
            scan.ai_comments = []

        scan.ai_comments.append(ai_comment)
        await scan.save()

        return ScanOut.model_validate(scan.model_dump())
    
    async def get_analysis_with_rules(self, scan_id: str) -> AnalysisWithRulesResponse:
        scan = await self.scans_repository.get_scan_by_id(scan_id)
        if not scan:
            raise not_found.ObjectNotFoundError("scan", "scan_id", scan_id)
        
        if not scan.analysis or not scan.analysis.warnings:
            return AnalysisWithRulesResponse(
                repo_url=scan.scanoptions.repo_url
                analysis=AnalysisSchema.model_validate(scan.analysis.model_dump()),
                rules=[]
            )

        rules_ids = list({w["rules_id"] for w in scan.analysis["warnings"] if "rules_id" in w})

        rules_service = RulesService()
        rules = await rules_service.get_rules_by_ids(rules_ids)

        return AnalysisWithRulesResponse(
            repo_url=scan.scanoptions.repo_url
            analysis=AnalysisSchema.model_validate(scan.analysis.model_dump()),
            rules=[RuleOut.model_validate(r.model_dump()) for r in rules]
        )