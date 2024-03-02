from typing import Any, TYPE_CHECKING

from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithTagId, MixinWithUnsubscribeOption
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class SubscribeToTag(MixinWithUnsubscribeOption, MixinWithTagId, BaseMethod[None]):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            method=("DELETE" if self.unsubscribe else "PUT"),
            url=DrukarniaEndpoints.SubscribeToTag.format(tag_id=self.tag_id),
            data={},
            **kwargs,
        )
