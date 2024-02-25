from typing import Any, Optional

from attr import field, frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@frozen
class ReplyToComment(BaseMethod[str]):
    article_id: str
    reply_to_comment_id: str
    comment_text: str
    owner_id: Optional[str]
    url: str = field(
        init=False,
        default="/api/articles/{article_id}/comments/{comment_id}/replies",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> str:
        response = await session.post(
            url=self.url.format(self.article_id, self.comment_text),
            data={
                "comment": self.comment_text,
                "replyToComment": self.reply_to_comment_id,
                "rootComment": self.reply_to_comment_id,  # not sure
                "rootCommentOwner": self.owner_id,
                "replyToUser": self.owner_id,
            },
            **kwargs,
        )

        data = await response.read()
        return data.decode("utf-8")
