from typing import List
from beanie import Document

class Scan(Document):
    scan_id: int
    rules_id: List[int]

    class Settings:
        name = "scans"