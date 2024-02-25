from typing import Any

from attrs import field, frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithArticleID, MixinWithCommentID
from drukarnia_api.network.session import DrukarniaSession


@frozen
class DeleteComment(MixinWithArticleID, MixinWithCommentID, BaseMethod[None]):
    url: str = field(
        init=False,
        default="/api/articles/{article_id}/comments/{comment_id}",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            "DELETE",
            self.url.format(article_id=self.article_id, comment_id=self.comment_id),
            data={},
            **kwargs,
        )
