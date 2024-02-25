from typing import Any, Generator

from attrs import field, frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPage
from drukarnia_api.models import ExtendedCardArticleModel
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class FindTags(
    MixinWithPage, BaseMethod[Generator[ExtendedCardArticleModel, None, None]]
):
    query: str
    with_relations: bool
    name: str
    url: str = field(
        init=False,
        default="/api/articles/search/tags",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[ExtendedCardArticleModel, None, None]:
        response = await session.get(
            self.url,
            data={},
            params={
                "text": self.query,
                "page": self.page,
            },
            **kwargs,
        )

        data_ = await response.json()
        return (ExtendedCardArticleModel(**data) for data in data_)
