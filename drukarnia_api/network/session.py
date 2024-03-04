from functools import partialmethod
from types import TracebackType
from typing import Any, Optional, Self, Type

from aiohttp import ClientResponse, ClientSession

from drukarnia_api.network.utils import _check_response


class DrukarniaSession:
    __slots__ = (
        "_session",
    )

    def __init__(self: Self) -> None:
        self._session: ClientSession = ClientSession(
            base_url="https://drukarnia.com.ua",
            trust_env=True,
        )

    async def __aenter__(self: Self) -> Self:
        await self._session.__aenter__()
        return self

    async def __call__(
        self: Self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> ClientResponse:
        response = await self._session.request(
            method=method,
            url=url,
            **kwargs,
        )

        await _check_response(response)
        return response

    post = partialmethod(__call__, method="POST")
    get = partialmethod(__call__, method="GET")
    patch = partialmethod(__call__, method="PATCH")
    put = partialmethod(__call__, method="PUT")
    delete = partialmethod(__call__, method="DELETE")

    async def __aexit__(
        self: Self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self._session.__aexit__(exc_type, exc_value, traceback)
