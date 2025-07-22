from beanie import Document
from pydantic import Field

class Counter(Document):
    key: str = Field(unique=True)
    counter: int = 0

    class Settings:
        name = "counters"
