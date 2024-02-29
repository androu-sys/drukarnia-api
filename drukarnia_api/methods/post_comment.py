from typing import Any, TYPE_CHECKING

from attrs import frozen, field, validators
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithArticleId
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class PostComment(MixinWithArticleId, BaseMethod[str]):
    comment_text: str = field(
        validator=validators.instance_of(str)
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> str:
        response = await session.post(
            url=DrukarniaEndpoints.PostComment.format(article_id=self.article_id),
            data={
                "comment": self.comment_text,
            },
            **kwargs,
        )

        posted_comment_id = await response.read()
        return str(posted_comment_id)
