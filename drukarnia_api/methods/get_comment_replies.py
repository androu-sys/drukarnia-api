from typing import Any, TYPE_CHECKING, Generator

from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import CommentModel
from drukarnia_api.methods.mixins import MixinWithArticleId, MixinWithCommentId
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen
class GetCommentReplies(
    MixinWithArticleId,
    MixinWithCommentId,
    BaseMethod[Generator[CommentModel, None, None]],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[CommentModel, None, None]:
        response = await session.post(
            url=DrukarniaEndpoints.GetCommentReplies.format(
                article_id=self.article_id,
                comment_id=self.comment_id,
            ),
            data={},
            **kwargs,
        )

        records = await response.json()
        return (CommentModel.from_json(record) for record in records)
