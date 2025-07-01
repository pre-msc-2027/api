from typing import List
from pydantic import BaseModel, Field

class ScanOptionsSchema(BaseModel):
    repo_url: str
    use_ai_assistance: bool
    max_depth: int
    follow_symlinks: bool
    target_type: str
    target_files: List[str]
    severity_min: str 
    branch_id: str
    commit_hash: str

class ScanCreate(BaseModel):
    scan_options: ScanOptionsSchema

class ScanOut(ScanCreate):
    scan_id: str
    id: str = Field(..., alias="_id")  # Automatically maps MongoDB's `_id` to `id`

    class Config:
        allow_population_by_field_name = True  # Enables FastAPI to return `id` instead of `_id`
        orm_mode = True