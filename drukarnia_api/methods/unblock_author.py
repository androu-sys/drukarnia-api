from typing import Any
from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.block_author import BlockAuthor
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class UnblockAuthor(BlockAuthor, BaseMethod[None]):
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
