from typing import Any, Generator

from attr import define, field

from drukarnia_api.dto import Article
from drukarnia_api.methods.base import BaseMethod, ResponseBase
from drukarnia_api.methods.mixins import MixinWithPage
from drukarnia_api.network.session import DrukarniaSession


@define
class GetReadsHistoryResponse(ResponseBase):
    reads: Generator[Article, None, None]


@define(frozen=True)
class GetReadsHistoryRequest(MixinWithPage, BaseMethod[GetReadsHistoryResponse]):
    url: str = field(
        init=False,
        default="/api/stats/reads/history",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        *args: Any,
        **kwargs: Any,
    ) -> GetReadsHistoryResponse:
        response = await session.get(
            data={},
            params={"page": self.page},
            *args,
            **kwargs,
        )

        authors = await response.json()
        return GetReadsHistoryResponse(
            reads = Article(**author) for author in authors
        )  # Change the model from Author to Notification
    
