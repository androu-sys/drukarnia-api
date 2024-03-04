from typing import TYPE_CHECKING, Any

from attrs import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithArticleSlug
from drukarnia_api.models import ArticleModel, SerializedModel, from_json
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetArticle(
    MixinWithArticleSlug,
    BaseMethod[ArticleModel],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> ArticleModel:
        response = await session.get(
            url=DrukarniaEndpoints.GetArticleInfo.format(slug=self.article_slug),    # type: ignore[str-format]
            data={},
            **kwargs,
        )

        record: SerializedModel = await response.json()
        return from_json(ArticleModel, record)
