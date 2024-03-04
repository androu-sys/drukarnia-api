from typing import TYPE_CHECKING, Any

from attrs import field, frozen, validators

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithArticleId
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class LikeArticle(
    MixinWithArticleId,
    BaseMethod[None],
):
    n_likes: int = field(
        validator=(
            validators.instance_of(int),
            validators.ge(val=0),
            validators.le(val=10),
        ),
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session.post(
            url=DrukarniaEndpoints.LikeArticle.format(article_id=self.article_id),    # type: ignore[str-format]
            data={
                "likes": self.n_likes,
            },
            **kwargs,
        )
