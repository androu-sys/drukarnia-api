from typing import Any, TYPE_CHECKING

from attrs import frozen, validators, field
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import ArticleModel
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen
class GetArticle(BaseMethod[ArticleModel]):
    article_slug: str = field(
        validator=validators.instance_of(str),
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> ArticleModel:
        response = await session.get(
            url=DrukarniaEndpoints.GetArticleInfo.format(slug=self.article_slug),
            data={},
            **kwargs,
        )

        record = await response.json()
        return ArticleModel.from_json(record)
