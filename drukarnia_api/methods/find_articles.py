from typing import Any, TYPE_CHECKING, Generator

from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import ArticleModel
from drukarnia_api.methods.mixins import MixinWithPagination, MixinWithQuery
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class FindArticle(
    MixinWithPagination,
    MixinWithQuery,
    BaseMethod[Generator[ArticleModel, None, None]],
): #
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[ArticleModel, None, None]:
        response = await session.get(
            url=DrukarniaEndpoints.FindArticles,
            data={},
            params={
                "name": self.query,
                "page": self.page,
            },
            **kwargs,
        )

        records = await response.json()
        return (ArticleModel.from_json(record) for record in records)
