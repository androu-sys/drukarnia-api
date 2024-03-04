from typing import TYPE_CHECKING, Any, Iterable

from attrs import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPagination
from drukarnia_api.models import ArticleModel, SerializedModel, from_json
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetReadsHistory(
    MixinWithPagination,
    BaseMethod[Iterable[ArticleModel]],
):

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Iterable[ArticleModel]:
        response = await session.get(
            url=DrukarniaEndpoints.GetReadsHistory,
            data={},
            params={"page": self.page},
            **kwargs,
        )

        articles: Iterable[SerializedModel] = await response.json()
        return (
            from_json(ArticleModel, article)
            for article in articles
        )
