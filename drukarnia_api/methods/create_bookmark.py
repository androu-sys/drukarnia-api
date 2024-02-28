from typing import Any, TYPE_CHECKING

from attrs import frozen, field, validators
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import BookmarkModel
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen
class CreateBookmark(BaseMethod[BookmarkModel]):
    name: str = field(validator=validators.instance_of(str))

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> BookmarkModel:
        response = await session.get(
            url=DrukarniaEndpoints.CreateNewBookmark,
            data={},
            params={"name": self.name},
            **kwargs,
        )

        bookmark_id = await response.read()
        return BookmarkModel(id_=bookmark_id.decode('utf-8'),)
