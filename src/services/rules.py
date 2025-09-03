from src.repositories.rules import RulesRepository
from src.generics import Service
from src.exceptions import not_found
from src.schemas.rule import RuleCreate, RuleOut
from src import models
from typing import List


class RulesService(Service):

    def __init__(self):
        self.rules_repository= RulesRepository()

    async def get_rule(self, rule_id: str) -> RuleOut:
        rule = await self.rules_repository.get_rule_by_id(rule_id)
        if rule is None:
            raise not_found.ObjectNotFoundError("rule", "rule_id", str(rule_id))
        return RuleOut.model_validate(rule.model_dump())

    async def create_rule(self, rule_create: RuleCreate) -> RuleOut:
        
        rule_model = models.Rule(**rule_create.model_dump())
        created = await self.rules_repository.create(rule_model)
        return RuleOut.model_validate(created.model_dump())

    async def get_rules_by_ids(self, rule_ids: List[str]) -> List[models.Rule]:
        return await self.rules_repository.get_by_ids(rule_ids)
    
    async def get_all_rules(self) -> List[models.Rule]:
        return await self.rules_repository.get_all()

    async def get_rules_by_scan(self, scan_id: str) -> List[models.Rule]:
        from .scans import ScansService
        scan = await self.scans_repository.get_scan_by_id(scan_id)
        if not scan:
            raise not_found.ObjectNotFoundError("scan", "scan_id", scan_id)
        rules_ids = scan.scan_options.rules_id
        return rules_ids