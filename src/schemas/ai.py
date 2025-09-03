from pydantic import BaseModel
from typing import List, Optional
from src.schemas.scan import AnalysisSchema
from src.schemas.rule import RuleOut

class AnalysisWithRulesResponse(BaseModel):
    repo_url: str
    analysis: Optional[AnalysisSchema] = None
    rules: Optional[List[RuleOut]] = None
