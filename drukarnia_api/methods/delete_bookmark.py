from typing import Any, TYPE_CHECKING

from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithBookmarkId
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen
class DeleteBookmark(MixinWithBookmarkId, BaseMethod[None]):

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session.delete(
            url=DrukarniaEndpoints.DeleteBookmark.format(bookmark_id=self.bookmark_id),
            data={},
            **kwargs,
        )
