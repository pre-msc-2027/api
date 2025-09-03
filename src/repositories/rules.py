from src.generics import Repository
from typing import Optional, List
from src.models.rule import Rule


class RulesRepository(Repository):

    def __init__(self):
        super().__init__(Rule)

    async def get_rule_by_id(self, rule_id: str) -> Optional[Rule]:
        return await Rule.find_one(Rule.rule_id == rule_id)

    async def create(self, rule: Rule) -> Rule:
        await rule.insert()
        return rule

    async def get_by_ids(self, ids: List[str]):
        return await Rule.find(Rule.rule_id.in_(ids)).to_list()

    async def get_all(self):
        return await Rule.find_all().to_list()

