from typing import Any, TYPE_CHECKING

from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithArticleId, MixinWithCommentText
from drukarnia_api.models import CommentModel
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class PostComment(
    MixinWithCommentText,
    MixinWithArticleId,
    BaseMethod[CommentModel],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> CommentModel:
        response = await session.post(
            url=DrukarniaEndpoints.PostComment.format(article_id=self.article_id),
            data={
                "comment": self.comment_text,
            },
            **kwargs,
        )

        posted_comment_id = await response.read()
        return CommentModel(id_=posted_comment_id.decode('utf-8'))
