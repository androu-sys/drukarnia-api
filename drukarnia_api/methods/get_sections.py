from typing import Generator, Any

from attr import define, field

from drukarnia_api.dto import Article
from drukarnia_api.methods import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPage
from drukarnia_api.network.session import DrukarniaSession


@define(frozen=True)
class GetReadsHistory(MixinWithPage, BaseMethod[Generator[Article, None, None]]):
    url: str = field(
        init=False,
        default="/api/stats/reads/history",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        *args: Any,
        **kwargs: Any,
    ) -> Generator[Article, None, None]:
        response = await session.get(
            data={},
            params={"page": self.page},
            *args,
            **kwargs,
        )

        articles = await response.json()
        return (
            Article(**article) for article in articles
        )  # Change the model from Author to Notification
    