from typing import Generic, TypeVar, Any, TYPE_CHECKING, Type
from abc import abstractmethod, ABC
from attr import define
from  aiohttp import ClientResponse

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


ResultType = TypeVar("ResultType", bound="ResponseBase")


class BaseMethod(ABC, Generic[ResultType]):
    __slots__ = ()

    async def __call__(self, session: "DrukarniaSession", **kwargs: Any) -> ResultType:
        return await self._request(session, **kwargs)

    @abstractmethod
    async def _request(self, session: "DrukarniaSession", *args: Any, **kwargs: Any) -> ResultType:
        raise NotImplementedError("Implement `_from_response` in child class.")


@define
class ResponseBase:
    status: int
    data: dict
    response: ClientResponse


    def __attrs_post_init__(self):
        if int(self.response.status) > 201:
            raise ValueError(
                self.data['message'], self.response.status,
                self.response.request_info.method, str(self.response.request_info.url)
                )


    @classmethod
    async def from_response(cls: Type[ResultType], response) -> ResultType:
        return cls(status=response.status, data=(await response.json()), response=response)
