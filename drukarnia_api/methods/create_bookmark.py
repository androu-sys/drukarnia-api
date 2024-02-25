from typing import Any

from attrs import frozen, field

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class CreateBookmark(BaseMethod[str]):
    name: str
    url: str = field(
        init=False,
        default="/api/articles/bookmarks/lists",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> str:
        response = await session.get(
            self.url,
            data={},
            params={"name": self.name},
            **kwargs,
        )

        bookmark_id = await response.read()
        return bookmark_id.decode('utf-8')
