from typing import Any
from attrs import frozen, field
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class DeleteSection(BaseMethod[None]):
    section_id: str
    url: str = field(
        init=False,
        default="/api/articles/bookmarks/lists/{section_id}",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            "DELETE",
            self.url.format(section_id=self.section_id),
            data={},
            **kwargs,
        )
