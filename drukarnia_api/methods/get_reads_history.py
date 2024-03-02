from typing import Any, TYPE_CHECKING, Generator

from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import ArticleModel
from drukarnia_api.methods.mixins import MixinWithPagination
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetReadsHistory(
    MixinWithPagination,
    BaseMethod[Generator[ArticleModel, None, None]],
):

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[ArticleModel, None, None]:
        response = await session.get(
            url=DrukarniaEndpoints.GetReadsHistory,
            data={},
            params={"page": self.page},
            **kwargs,
        )

        articles = await response.json()
        return (ArticleModel.from_json(article) for article in articles)
