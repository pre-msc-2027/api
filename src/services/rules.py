from src.generics import Service
from src.repositories import RulesRepository
from src.exceptions import not_found
from src.schemas.rule import RuleCreate, RuleOut
from src import models
from beanie import PydanticObjectId
from typing import List


class RulesService(Service):

    rules_repository: RulesRepository

    async def get_rule(self, rule_id: PydanticObjectId) -> RuleOut:
        rule = await self.rules_repository.get_rule_by_id(rule_id)
        if rule is None:
            raise not_found.ObjectNotFoundError("rule", "rule_id", str(rule_id))
        return RuleOut.model_validate(rule)

    async def create_rule(self, rule_create: RuleCreate) -> RuleOut:
        # Create Beanie model from schema
        rule_model = models.Rule(**rule_create.model_dump())
        created = await self.rules_repository.create(rule_model)
        return RuleOut.model_validate(created)

    async def get_rules(self) -> List[PydanticObjectId]:
        return await self.rules_repository.get_all()