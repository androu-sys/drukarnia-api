from typing import Any, TYPE_CHECKING

from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithAuthorId, MixinWithUnblockOption
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class BlockAuthor(
    MixinWithAuthorId,
    MixinWithUnblockOption,
    BaseMethod[None],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            method=("PUT" if self.unblock else "PATCH"),
            url=DrukarniaEndpoints.BlockAuthor.format(author_id=self.author_id),
            data={},
            **kwargs,
        )
