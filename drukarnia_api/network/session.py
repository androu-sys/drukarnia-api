from typing import Any, Optional, Self, Type

from aiohttp import ClientSession
from aiohttp.cookiejar import SimpleCookie
from aiohttp import ClientResponse

class DrukarniaSession:
    __slots__ = (
        "_session",
    )

    def __init__(self) -> None:
        self._session: ClientSession = ClientSession(
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
    ) -> ClientResponse:
        return await self._session.request(
            method=method,
            url=url,
            **kwargs,
        )

    async def get(
        self,
        url: str,
        **kwargs,
    ) -> ClientResponse:
        return await self.__call__(
            method="GET",
            url=url,
            **kwargs,
        )

    async def post(
        self,
        url: str,
        **kwargs,
    ) -> ClientResponse:
        return await self.__call__(
            method="POST",
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


    async def set_cookie(self, cookies: SimpleCookie) -> None:
        self._session.cookie_jar.update_cookies(cookies=cookies)
