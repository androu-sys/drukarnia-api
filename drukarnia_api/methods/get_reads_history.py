from typing import Any, Generator

from attrs import frozen, field

from drukarnia_api.models import ArticleSummaryModel
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPage
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetReadsHistory(MixinWithPage, BaseMethod[Generator[ArticleSummaryModel, None, None]]):
    url: str = field(
        init=False,
        default="/api/stats/reads/history",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[ArticleSummaryModel, None, None]:
        response = await session.get(
            self.url,
            data={},
            params={"page": self.page},
            **kwargs,
        )

        articles = await response.json()
        return (ArticleSummaryModel(**article) for article in articles)
