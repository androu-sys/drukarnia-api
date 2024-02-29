from typing import Any, TYPE_CHECKING

from attrs import frozen, field
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithArticleId, MixinWithCommentId
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen
class LikeComment(
    MixinWithArticleId,
    MixinWithCommentId,
    BaseMethod[None],
):
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
            url=DrukarniaEndpoints.LikeComment.format(
                article_id=self.article_id,
                comment_id=self.comment_id,
            ),
            data={},
            **kwargs,
        )
