from pydantic import BaseModel, Field

class RuleBase(BaseModel):
    rule_id: int
    name: str
    description: str | None = None

class RuleCreate(RuleBase):
    pass

class RuleOut(RuleBase):
    id: str = Field(..., alias="_id")  # Automatically maps MongoDB's `_id` to `id`

    class Config:
        allow_population_by_field_name = True  # Enables FastAPI to return `id` instead of `_id`
        orm_mode = True