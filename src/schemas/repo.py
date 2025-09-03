from typing import List, Any, Optional
from pydantic import BaseModel


class RuleParameterSchema(BaseModel):
    name: str
    value: Any


class RepoRuleSchema(BaseModel):
    rule_id: str
    parameters: List[RuleParameterSchema] = []


class RepoUserSchema(BaseModel):
    user_id: str
    email: str
    name: Optional[str] = None


class RepoBase(BaseModel):
    user: RepoUserSchema
    repo_url: str
    branches_id: List[str]
    rules: List[RepoRuleSchema]


class RepoCreate(RepoBase):
    pass


class RepoOut(RepoBase):
    pass
