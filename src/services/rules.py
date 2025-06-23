from src.generics import Service
from src.repositories import RulesRepository
from src.exceptions import not_found
from src.schemas.rule import RuleCreate, RuleDbId
from src.models.rule import rule


class RulesService(Service):

    rules_repository: RulesRepository

    async def get_rule(self, rule_id: int) -> RuleDbId:
        rule = await self.rules_repository.get_rule_by_rule_id(rule_id)
        if rule is None:
            raise not_found.ObjectNotFoundError("rule", "rule_id", rule_id)
        return RuleDbId.model_validate(rule)

    async def create_rule(self, rule_create: RuleCreate) -> RuleDbId:
        data = rule_create.model_dump()
        created = await self.rules_repository.create(data)
        return RuleDbId.model_validate(created)

    async def get_rules(self) -> list[int]:
        rules = await self.rules_repository.get_all()
        return [rule.rule_id for rule in rules]