from beanie import Document

class Rule(Document):
    rule_id: int
    name: str
    description: str | None = None

    class Settings:
        name = "rules"