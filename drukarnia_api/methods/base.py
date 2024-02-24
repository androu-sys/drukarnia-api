from typing import Generic, TypeVar, Any
from drukarnia_api.network.session import BaseSession
from abc import abstractmethod, ABC


ResultType = TypeVar("ResultType", bound=Any)


class Request(ABC, Generic[ResultType]):
    def __init__(self, ):

    async def __call__(self, session: BaseSession, *args: Any, **kwargs: Any) -> ResultType:
        return await self._from_response(session, *args, **kwargs)

    @abstractmethod
    async def _from_response(self, session: BaseSession, *args: Any, **kwargs: Any) -> ResultType:
        raise NotImplementedError("Implement `_from_response` in child class.")
