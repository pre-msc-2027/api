from beanie import PydanticObjectId
from typing import Optional

from src import models


class ruleRepository:

    async def get_rule_by_id(self, rule_id: PydanticObjectId) -> Optional[models.rule]:
        return await models.rule.get(rule_id)

    async def create_rule(self, rule: models.rule) -> models.rule:
        await rule.insert()
        return rule

    async def get_rules(self) -> list[PydanticObjectId]:
        rules = await models.rule.find_all().to_list()
        return [rule.id for rule in rules]
