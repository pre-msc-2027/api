from pydantic import BaseModel

class RuleBase(BaseModel):
    rule_id: int
    name: str
    description: str | None = None

class RuleCreate(RuleBase):
    pass

class RuleDbId(RuleBase):
    id: str  # MongoDB ID