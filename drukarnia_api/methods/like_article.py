from typing import Any

from attr import field, frozen, validators

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithArticleID
from drukarnia_api.network.session import DrukarniaSession


@frozen
class LikeArticle(MixinWithArticleID, BaseMethod[None]):
    n_likes: int = field(
        validator=(
            validators.instance_of(int),
            validators.gt(val=0),
            validators.le(val=10),
        ),
    )
    url: str = field(init=False, default="/api/articles/{article_id}/like")

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session.post(
            url=self.url.format(self.article_id),
            data={"likes": int(self.n_likes)},
            **kwargs,
        )
