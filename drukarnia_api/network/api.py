from typing import Self, Optional, Type, Any
from drukarnia_api.methods.base import BaseMethod, ResultType
from drukarnia_api.network.session import DrukarniaSession


class API:
    __slots__ = (
        "_session",
    )

    def __init__(self, session: DrukarniaSession = None):
        self._session = session if session else DrukarniaSession()

    async def __call__(
        self,
        method: BaseMethod[ResultType],
        **kwargs: Any,
    ) -> ResultType:
        return await method(self._session, **kwargs)

    async def __aenter__(self) -> Self:
        await self._session.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Any,
    ) -> None:
        await self._session.__aexit__(exc_type, exc_value, traceback)
