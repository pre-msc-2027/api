import typing
from abc import ABC

from typing import Final, Any

from src.exceptions.base import BaseServiceException, param


class BaseNotFoundError(BaseServiceException, ABC):

    STATUS_CODE: Final[int] = 404


class ObjectNotFoundError(BaseNotFoundError):

    PATTERN = f"{param('obj')} not found with '{param('key')}' = '{param('value')}'"
    ERROR_CODE: typing.Final[int] = 0

    obj: str
    key: str
    value: Any

    def __init__(self, obj: str, key: str, value: Any):

        self.obj = obj
        self.key = key
        self.value = value

        super().__init__(obj=obj, key=key, value=value)