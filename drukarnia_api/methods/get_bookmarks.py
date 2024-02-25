from typing import Any, Generator

from attrs import frozen, field

from drukarnia_api.models import BookmarkModel
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetBookmarks(BaseMethod[Generator[BookmarkModel, None, None]]):
    preview: bool = True
    url: str = field(
        init=False,
        default="/api/articles/bookmarks/lists",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[BookmarkModel, None, None]:
        response = await session.get(
            self.url,
            data={},
            params={"preview": self.preview},
            **kwargs,
        )

        articles = await response.json()
        return (BookmarkModel.from_json(article) for article in articles)
