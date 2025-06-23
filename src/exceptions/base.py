
from abc import ABC, abstractmethod
from functools import reduce

from fastapi import HTTPException

from typing import Any

def param(key: str): return rf"(?P<{key}>.+)"

def _format(pattern: str, values: dict[str, Any]) -> str:
    return reduce(lambda p, kv: p.replace(param(kv[0]), kv[1], 1), values.items(), pattern).replace('\\', '')


class BaseServiceException(Exception, ABC):

    STATUS_CODE: int
    ERROR_CODE: int
    PATTERN: str

    message: str
    params: dict[str, Any]

    def __init__(self, **params):

        self.message = _format(self.PATTERN, params)
        self.params = params

        super().__init__(self.message)

    def get_response(self) -> HTTPException:
        return HTTPException(status_code=self.STATUS_CODE, detail=self.get_body())

    def get_body(self) -> str | dict[str, Any]:
        return {'code': self.ERROR_CODE, 'message': str(self), 'params': self.params}
