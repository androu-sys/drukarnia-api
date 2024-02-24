from typing import Generic, TypeVar, Any, TYPE_CHECKING
from abc import abstractmethod, ABC

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


ResultType = TypeVar("ResultType", bound=Any)


class BaseMethod(ABC, Generic[ResultType]):
    __slots__ = ()

    async def __call__(self, session: "DrukarniaSession", **kwargs: Any) -> ResultType:
        return await self._from_response(session, **kwargs)

    @abstractmethod
    async def _from_response(self, session: "DrukarniaSession", *args: Any, **kwargs: Any) -> ResultType:
        raise NotImplementedError("Implement `_from_response` in child class.")
