from beanie import Document
from typing import List, Any, Dict, Optional
from pydantic import BaseModel


class RuleParameter(BaseModel):
    type: str
    name: str
    default: Any
    description: Optional[str] = None
    options: Optional[Dict[str, Any]] = None


class Rule(Document):
    rule_id: str
    name: str
    slang: str
    description: Optional[str] = None
    tags: List[str] = []
    parameters: List[RuleParameter] = []

    class Settings:
        name = "rules"