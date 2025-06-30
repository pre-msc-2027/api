from fastapi import APIRouter, Depends
from typing import List
from src.schemas import RuleCreate, RuleOut 
from src.services import RulesService
from src.exceptions import not_found

router = APIRouter(prefix="/rules", tags=["rules"])

@router.get("/", response_model=List[RuleOut])
async def get_all_rules(service: RulesService = Depends(RulesService)):
    rule_ids = await service.get_rules()
    rules = [await service.get_rule(rid) for rid in rule_ids]
    return rules


@router.get("/{rule_id}", response_model=RuleOut)
async def get_rule(rule_id: str, service: RulesService = Depends(RulesService)):
    try:
        return await service.get_rule(rule_id)
    except not_found.ObjectNotFoundError as e:
        raise e.get_response()


@router.post("/", response_model=RuleOut, status_code=201)
async def create_rule(rule: RuleCreate, service: RulesService = Depends(RulesService)):
    return await service.create_rule(rule)
