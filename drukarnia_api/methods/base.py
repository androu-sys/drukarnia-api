from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


ResultType = TypeVar("ResultType", bound=Any)


class BaseMethod(ABC, Generic[ResultType]):
    __slots__ = ()

    async def __call__(self, session: "DrukarniaSession", **kwargs: Any) -> ResultType:
        return await self._request(session, **kwargs)

    @abstractmethod
    async def _request(self, session: "DrukarniaSession", **kwargs: Any) -> ResultType:
        msg = "Implement `_request` in child class."
        raise NotImplementedError(msg)
