from typing import TYPE_CHECKING, Any

from attrs import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithTagId, MixinWithUnblockOption
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class BlockTag(
    MixinWithTagId,
    MixinWithUnblockOption,
    BaseMethod[None],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session.put(
            url=DrukarniaEndpoints.BlockTag.format(tag_id=self.tag_id),    # type: ignore[str-format]
            data={
                "isBlocked": not self.unblock,
            },
            **kwargs,
        )
