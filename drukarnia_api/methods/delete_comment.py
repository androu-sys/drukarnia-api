from typing import TYPE_CHECKING, Any

from attrs import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithArticleId, MixinWithCommentId
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class DeleteComment(
    MixinWithCommentId,
    MixinWithArticleId,
    BaseMethod[None],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session.delete(
            url=DrukarniaEndpoints.DeleteComment.format(
                article_id=self.article_id,
                comment_id=self.comment_id,
            ),    # type: ignore[str-format]
            data={},
            **kwargs,
        )
