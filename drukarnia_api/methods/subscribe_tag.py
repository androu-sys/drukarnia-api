from typing import Any

from attrs import frozen, field, validators
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@frozen
class SubscribeTag(BaseMethod[None]):
    tag_id: str = field(validator=validators.instance_of(str))
    url: str = field(
        init=False,
        default="/api/preferences/tags/{tag_id}",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            "PUT",
            self.url.format(tag_id=self.tag_id),
            data={},
            **kwargs,
        )
