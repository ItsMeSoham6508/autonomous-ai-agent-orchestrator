from http import HTTPStatus
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')

class StandardResponse(BaseModel, Generic[T]):
    data: T
    message: str
    status: HTTPStatus