from typing import TYPE_CHECKING, Any

from attrs import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithArticleId, MixinWithCommentId, MixinWithUnlikeOption
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class LikeComment(    # type: ignore[misc]
    MixinWithUnlikeOption,
    MixinWithArticleId,
    MixinWithCommentId,
    BaseMethod[None],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            method=("DELETE" if self.unlike else "POST"),
            url=DrukarniaEndpoints.LikeComment.format(
                article_id=self.article_id,
                comment_id=self.comment_id,
            ),    # type: ignore[str-format]
            data={},
            **kwargs,
        )
