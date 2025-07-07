from typing import List
from pydantic import BaseModel

class RepoBase(BaseModel):
    repo_url: str
    user: str
    rules_list: List[int]

class RepoCreate(RepoBase):
    pass

class RepoOut(RepoBase):
    pass 
