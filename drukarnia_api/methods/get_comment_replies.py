from typing import TYPE_CHECKING, Any, Iterable

from attrs import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithArticleId, MixinWithCommentId
from drukarnia_api.models import CommentModel, SerializedModel, from_json
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetCommentReplies(
    MixinWithArticleId,
    MixinWithCommentId,
    BaseMethod[Iterable[CommentModel]],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Iterable[CommentModel]:
        response = await session.post(
            url=DrukarniaEndpoints.GetCommentReplies.format(
                article_id=self.article_id,
                comment_id=self.comment_id,
            ),    # type: ignore[str-format]
            data={},
            **kwargs,
        )

        records: Iterable[SerializedModel] = await response.json()
        return (
            from_json(CommentModel, record)
            for record in records
        )
