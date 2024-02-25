from typing import Any

from attr import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.like_comment import LikeComment
from drukarnia_api.network.session import DrukarniaSession


@frozen
class RemoveLikes(LikeComment, BaseMethod[None]):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            "DELETE",
            url=self.url.format(self.article_id, self.comment_id),
            data={},
            **kwargs,
        )
