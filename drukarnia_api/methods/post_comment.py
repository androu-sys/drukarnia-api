from typing import Any

from attr import field, frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@frozen
class PostComment(BaseMethod[str]):
    article_id: str
    comment_text: str

    url: str = field(init=False, default="/api/articles/{article_id}/comments")

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> str:
        response = await session.post(
            url=self.url.format(self.article_id),
            data={"comment": self.comment_text},
            **kwargs,
        )

        posted_comment_id = await response.read()
        return str(posted_comment_id)
