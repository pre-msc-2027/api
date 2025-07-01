from typing   import List
from beanie   import Document
from pydantic import BaseModel

class ScanOptions(BaseModel):
    repo_url: str
    use_ai_assistance: bool
    max_depth: int
    follow_symlinks: bool
    target_type: str 
    target_files: List[str]
    severity_min: str 
    branch_id: int
    commit_hash: str

class Scan(Document):
    scan_id: int  
    scan_options: ScanOptions

    class Settings:
        name = "scans"