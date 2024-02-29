from typing import Any, TYPE_CHECKING

from attrs import frozen
from drukarnia_api.methods.like_comment import LikeComment
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen
class RemoveLikeFromComment(LikeComment, BaseMethod[None]):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session.delete(
            url=DrukarniaEndpoints.RemoveLikeFromComment.format(
                article_id=self.article_id,
                comment_id=self.comment_id,
            ),
            data={},
            **kwargs,
        )
