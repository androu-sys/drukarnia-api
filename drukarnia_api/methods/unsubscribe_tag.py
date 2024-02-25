from typing import Any
from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.subscribe_tag import SubscribeTag
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class UnsubscribeTag(SubscribeTag, BaseMethod[None]):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            "DELETE",
            self.url.format(tag_id=self.tag_id),
            data={},
            **kwargs,
        )
