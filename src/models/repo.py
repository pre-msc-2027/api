from typing import List
from beanie import Document

class Repo(Document):
    repo_url: str
    user: str
    rules_list: List[int]

    class Settings:
        name = "repos"