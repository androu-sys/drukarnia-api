from typing import Any

from attr import field, frozen, validators

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import ArticleModel
from drukarnia_api.network.session import DrukarniaSession


@frozen
class GetArticle(BaseMethod[ArticleModel]):
    article_id: str
    slug: str
    return_: bool = field(validator=validators.instance_of(bool))
    url: str = field(init=False, default="/api/articles/{slug}")

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> ArticleModel:
        response = await session.get(
            url=self.url.format(slug=self.slug),
            data={},
            **kwargs,
        )

        data = await response.json()
        return ArticleModel.from_json(**data)
