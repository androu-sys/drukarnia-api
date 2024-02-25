from typing import Any, Generator

from attrs import frozen, field

from drukarnia_api.models import SectionModel
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetSections(BaseMethod[Generator[SectionModel, None, None]]):
    preview: bool = True
    url: str = field(
        init=False,
        default="/api/articles/bookmarks/lists",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[SectionModel, None, None]:
        response = await session.get(
            self.url,
            data={},
            params={"preview": self.preview},
            **kwargs,
        )

        articles = await response.json()
        return (SectionModel.from_json(article) for article in articles)
