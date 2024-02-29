from typing import Any, TYPE_CHECKING

from attrs import frozen, field, validators
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import CommentModel
from drukarnia_api.methods.mixins import MixinWithArticleId, MixinWithCommentId, MixinWithAuthorId
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class ReplyToComment(
    MixinWithArticleId,
    MixinWithCommentId,
    MixinWithAuthorId,
    BaseMethod[CommentModel],
):
    comment_text: str = field(
        validator=validators.instance_of(str)
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> CommentModel:
        response = await session.post(
            url=DrukarniaEndpoints.ReplyToComment.format(
                article_id=self.article_id,
                comment_id=self.comment_id,
            ),
            data={
                "comment": self.comment_text,
                "replyToComment": self.comment_id,
                "replyToUser": self.author_id,
                "rootComment": self.comment_id,     # Not sure
                "rootCommentOwner": self.author_id,     # Not sure
            },
            **kwargs,
        )

        data = await response.read()
        return CommentModel(id_=data.decode("utf-8"))
