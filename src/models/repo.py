from typing import List, Any
from beanie import Document
from pydantic import BaseModel


class RuleParameter(BaseModel):
    name: str
    value: Any


class RepoRule(BaseModel):
    rule_id: str
    parameters: List[RuleParameter] 


class RepoUser(BaseModel):
    id: str 
    email: str
    name: str | None


class Repo(Document):
    user: RepoUser
    repo_url: str
    rules: List[RepoRule]

    class Settings:
        name = "repos"