from typing import Generator, Any

from attr import define, field

from drukarnia_api.models import SectionModel
from drukarnia_api.methods import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPage
from drukarnia_api.network.session import DrukarniaSession


@define(frozen=True)
class GetReadsHistory(MixinWithPage, BaseMethod[Generator[SectionModel, None, None]]):
    url: str = field(
        init=False,
        default="/api/stats/reads/history",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[SectionModel, None, None]:
        response = await session.get(
            data={},
            params={"page": self.page},
            **kwargs,
        )

        articles = await response.json()
        return (SectionModel(**article) for article in articles)
    