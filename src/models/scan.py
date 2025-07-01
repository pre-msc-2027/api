from typing import List, Optional
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field


class ScanOptions(BaseModel):
    repo_url: str
    use_ai_assistance: bool
    max_depth: int
    follow_symlinks: bool
    target_type: str
    target_files: Optional[List[str]]
    severity_min: str
    branch_id: str
    commit_hash: str


class Vulnerability(BaseModel):
    file: str
    line: int
    type: str
    severity: str
    description: str
    recommendation: str


class AnalysisSummary(BaseModel):
    total_files: int
    files_with_vulnerabilities: int
    vulnerabilities_found: int


class Analysis(BaseModel):
    status: str
    summary: AnalysisSummary
    vulnerabilities: List[Vulnerability]


class DependencyVulnerability(BaseModel):
    cve_id: str
    severity: str
    description: str
    recommendation: str


class Dependency(BaseModel):
    name: str
    version: str
    vulnerability: DependencyVulnerability


class AuthContext(BaseModel):
    user_id: str
    user_role: str
    session_id: str


class Scan(Document):
    scan_id: str
    timestamp: datetime
    project_name: str
    scanned_by: str
    scan_options: ScanOptions
    analysis: Optional[Analysis]
    ai_comments: Optional[str]
    scan_version: str
    dependencies: Optional[List[Dependency]]
    notes: Optional[str]
    auth_context: Optional[AuthContext]

    class Settings:
        name = "scans"
