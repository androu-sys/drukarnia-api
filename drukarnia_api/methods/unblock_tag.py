from typing import Any
from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.block_tag import BlockTag
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class UnblockTag(BlockTag, BaseMethod[None]):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            "PUT",
            self.url.format(tag_id=self.tag_id),
            data={"isBlocked": False},
            **kwargs,
        )
