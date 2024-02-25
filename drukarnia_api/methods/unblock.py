from typing import Any
from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.block import Block
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class Unblock(Block, BaseMethod[None]):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            "PUT",
            self.url.format(author_id=self.author_id),
            data={},
            **kwargs,
        )
