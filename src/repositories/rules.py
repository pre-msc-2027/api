from generics import Repository
from beanie import PydanticObjectId
from typing import Optional, List
from src import models


class RulesRepository(Repository):

    def __init__(self):
        super().__init__(models.Rule)

    async def get_rule_by_id(self, rule_id: PydanticObjectId) -> Optional[models.Rule]:
        return await models.Rule.get(rule_id)

    async def create(self, rule: models.Rule) -> models.Rule:
        await rule.insert()
        return rule

    async def get_all(self) -> List[PydanticObjectId]:
        rules = await models.Rule.find_all().to_list()
        return [rule.id for rule in rules]