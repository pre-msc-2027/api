import abc
from typing import Generic, TypeVar, Type
from beanie import Document

DocType = TypeVar("DocType", bound=Document)

class Repository(Generic[DocType], abc.ABC):
    def __init__(self, model: Type[DocType]):
        self.model = model

    async def get_by_id(self, id: int) -> DocType:
        return await self.model.get(id)

    async def get_all(self) -> list[DocType]:
        return await self.model.find_all().to_list()

    async def create(self, data: dict) -> DocType:
        doc = self.model(**data)
        await doc.insert()
        return doc
