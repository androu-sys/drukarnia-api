from typing import Any

from attr import field, frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithArticleID, MixinWithCommentID
from drukarnia_api.network.session import DrukarniaSession


@frozen
class LikeComment(MixinWithArticleID, MixinWithCommentID, BaseMethod[None]):
    url: str = field(
        init=False,
        default="/api/articles/{article_id}/comments/{comment_id}/likes",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session.post(
            url=self.url.format(self.article_id, self.comment_id),
            data={},
            **kwargs,
        )
