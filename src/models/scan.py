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
    rules_id: List[str] 
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

class Warning(BaseModel):
    file: str
    line: int
    rule_id: int
    id: int

class AnalysisSummary(BaseModel):
    total_files: int
    files_with_vulnerabilities: int
    vulnerabilities_found: int


class Analysis(BaseModel):
    status: str
    summary: AnalysisSummary
    vulnerabilities: List[Vulnerability]
    warnings: List[Warning]


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

class LogEntry(BaseModel):
    timestamp: str 
    message: str
    error: Optional[str] = None

class AIComment(BaseModel):
    warning_id: int
    original: str
    fixed: str

class Scan(Document):
    scan_id: str
    timestamp: datetime
    project_name: str
    scanned_by: str
    scan_options: ScanOptions
    analysis: Optional[Analysis] = None
    ai_comments: Optional[List[AIComment]] = None
    scan_version: str
    dependencies: Optional[List[Dependency]] = None
    notes: Optional[str] = None
    auth_context: Optional[AuthContext] = None
    logs: Optional[List[LogEntry]] = None

    class Settings:
        name = "scans"
