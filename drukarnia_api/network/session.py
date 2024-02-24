from typing import Self, Optional, Type, Any
from aiohttp import ClientSession


class DrukarniaSession:
    __slots__ = (
        "_session",
    )

    def __init__(self) -> None:
        self._session = ClientSession(
            base_url="https://drukarnia.com.ua",
            trust_env=True,
        )

    async def __aenter__(self) -> Self:
        await self._session.__aenter__()
        return self

    async def __call__(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> Any:
        return await self._session.request(
            method=method,
            url=url,
            **kwargs,
        )

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Any,
    ) -> None:
        await self._session.__aexit__(exc_type, exc_value, traceback)
