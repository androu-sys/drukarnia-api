from typing import Any

from attr import field, frozen, validators

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@frozen
class Bookmark(BaseMethod[None]):
    article_id: str
    section_id: str = field(validator=validators.instance_of(str))
    url: str = field(
        init=False, default="/api/articles/{article_id}/bookmarks"
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session.post(
            url="/api/articles/bookmarks",
            data={"article": self.article_id, "list": self.section_id},
            **kwargs,
        )
