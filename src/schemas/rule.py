from pydantic import BaseModel
from typing import List, Any, Dict, Optional


class RuleParameterSchema(BaseModel):
    type: str
    name: str
    default: Any
    description: Optional[str] = None
    options: Optional[Dict[str, Any]] = None


class RuleBase(BaseModel):
    rule_id: str
    name: str
    slang: str
    language: str
    description: Optional[str] = None
    tags: List[str] = []
    parameters: List[RuleParameterSchema] = []


class RuleCreate(RuleBase):
    pass


class RuleOut(RuleBase):
    pass