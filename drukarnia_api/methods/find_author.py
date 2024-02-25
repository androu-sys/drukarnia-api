from typing import Any, Generator

from attrs import field, frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPage
from drukarnia_api.models import SearchResultedAuthorModel
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class FindAuthor(
    MixinWithPage, BaseMethod[Generator[SearchResultedAuthorModel, None, None]]
):
    query: str
    with_relations: bool
    name: str
    url: str = field(
        init=False,
        default="/api/users/info",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[SearchResultedAuthorModel, None, None]:
        response = await session.get(
            self.url,
            data={},
            params={
                "name": self.query,
                "withRelationships": self.with_relations,
                "page": self.page,
            },
            **kwargs,
        )

        data_ = await response.json()
        return (SearchResultedAuthorModel(**data) for data in data_)
