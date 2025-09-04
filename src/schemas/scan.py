from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class ScanOptionsSchema(BaseModel):
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


class VulnerabilitySchema(BaseModel):
    file: str
    line: int
    type: str
    severity: str
    description: str
    recommendation: str

class WarningSchema(BaseModel):
    file: str
    line: int
    rule_id: str
    id: int

class AnalysisSummarySchema(BaseModel):
    total_files: int
    files_with_vulnerabilities: int
    vulnerabilities_found: int


class AnalysisSchema(BaseModel):
    status: str
    summary: AnalysisSummarySchema
    vulnerabilities: List[VulnerabilitySchema]
    warnings: List[WarningSchema]


class DependencyVulnerabilitySchema(BaseModel):
    cve_id: str
    severity: str
    description: str
    recommendation: str


class DependencySchema(BaseModel):
    name: str
    version: str
    vulnerability: DependencyVulnerabilitySchema


class AuthContextSchema(BaseModel):
    user_id: str
    user_role: str
    session_id: str

class LogEntrySchema(BaseModel):
    timestamp: str  
    message: str
    error: Optional[str] = None

class AnalysisSummaryItem(BaseModel):
    scan_id: str
    project_name: str
    branch_id: str

class RepoSummary(BaseModel):
    repo_url: str
    branches_id: List[str]
    analyses: List[AnalysisSummaryItem]

class AICommentSchema(BaseModel):
    warning_id: int
    original: str
    fixed: str


class ScanBase(BaseModel):
    project_name: str
    scanned_by: str
    scan_options: ScanOptionsSchema
    scan_version: str
    auth_context: Optional[AuthContextSchema] = None
    notes: Optional[str] = None
    token: str = None

class ScanCreate(ScanBase):
    token: str = None

class ScanOut(ScanBase):
    scan_id: str
    timestamp: datetime
    analysis: Optional[AnalysisSchema] = None
    ai_comments: Optional[List[AICommentSchema]] = None
    dependencies: Optional[List[DependencySchema]] = None
    logs: Optional[List[LogEntrySchema]] = None