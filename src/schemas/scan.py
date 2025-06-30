from typing import List
from pydantic import BaseModel, Field

class ScanBase(BaseModel):
    rules_id: List[int]

class ScanCreate(ScanBase):
    pass

class ScanOut(ScanBase):
    scan_id: int
    id: str = Field(..., alias="_id")  # Automatically maps MongoDB's `_id` to `id`

    class Config:
        allow_population_by_field_name = True  # Enables FastAPI to return `id` instead of `_id`
        orm_mode = True