from src.repositories.rules import RulesRepository
from src.generics import Service
from src.exceptions import not_found
from src.schemas.rule import RuleCreate, RuleOut
from src import models
from typing import List


class RulesService(Service):

    def __init__(self):
        self.rules_repository= RulesRepository()

    async def get_rule(self, rule_id: int) -> RuleOut:
        rule = await self.rules_repository.get_rule_by_id(rule_id)
        if rule is None:
            raise not_found.ObjectNotFoundError("rule", "rule_id", str(rule_id))
        return RuleOut.model_validate(rule.model_dump())

    async def create_rule(self, rule_create: RuleCreate) -> RuleOut:
        
        rule_model = models.Rule(**rule_create.model_dump())
        created = await self.rules_repository.create(rule_model)
        return RuleOut.model_validate(created.model_dump())

    async def get_rules_by_ids(self, rule_ids: List[int]) -> List[models.Rule]:
        return await self.rules_repository.get_by_ids(rule_ids)
    
    async def get_all_rules(self) -> List[models.Rule]:
        return await self.rules_repository.get_all()