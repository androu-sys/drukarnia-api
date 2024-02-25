from typing import Any
from attrs import frozen, field
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class DeleteBookmark(BaseMethod[None]):
    bookmark_id: str
    url: str = field(
        init=False,
        default="/api/articles/bookmarks/lists/{bookmark_id}",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            "DELETE",
            self.url.format(bookmark_id=self.bookmark_id),
            data={},
            **kwargs,
        )
