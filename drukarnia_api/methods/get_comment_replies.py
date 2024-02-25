from typing import Any, Generator

from attr import field, frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession
from drukarnia_api.models import CommentModel

@frozen
class GetCommentReplies(BaseMethod[Generator[CommentModel, None, None]]):
    article_id: str
    comment_id: str
    url: str = field(
        init=False,
        default="/api/articles/{article_id}/comments/{comment_id}/replies",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[CommentModel, None, None]:
        response = await session.post(
            url=self.url.format(self.article_id, self.comment_id),
            data={},
            **kwargs,
        )

        data_ = await response.json()
        return (CommentModel(**data) for data in data_)
