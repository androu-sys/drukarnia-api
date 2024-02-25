from typing import Any

from attrs import frozen, field

from drukarnia_api.models import SectionModel
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class CreateSection(BaseMethod[SectionModel]):
    name: str
    url: str = field(
        init=False,
        default="/api/articles/bookmarks/lists",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> SectionModel:
        response = await session.get(
            self.url,
            data={},
            params={"name": self.name},
            **kwargs,
        )

        bookmark_id = await response.read()
        return SectionModel(
            bookmark_id=bookmark_id.decode('utf-8'),
        )
