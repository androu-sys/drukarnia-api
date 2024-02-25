from typing import Any

from attr import field, frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.bookmark import Bookmark
from drukarnia_api.network.session import DrukarniaSession


@frozen
class UnBookmark(Bookmark, BaseMethod[None]):
    url: str = field(init=False, default="/api/articles/{article_id}/bookmarks")

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            "DELETE",
            self.url.format(article_id=self.article_id),
            data={},
            **kwargs,
        )
