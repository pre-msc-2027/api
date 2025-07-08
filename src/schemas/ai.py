from pydantic import BaseModel
from typing import List
from src.schemas.scan import AnalysisSchema
from src.schemas.rule import RuleOut

class AnalysisWithRulesResponse(BaseModel):
    analysis: AnalysisSchema
    rules: List[RuleOut]
