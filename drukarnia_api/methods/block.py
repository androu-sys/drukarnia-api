from typing import Any

from attrs import frozen, field
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class Block(BaseMethod[None]):
    author_id: str
    url: str = field(
        init=False,
        default="/api/relationships/block/{author_id}",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            "PATCH",
            self.url.format(author_id=self.author_id),
            data={},
            **kwargs,
        )
