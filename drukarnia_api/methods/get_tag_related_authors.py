from typing import Any, TYPE_CHECKING, Generator

from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import AuthorModel
from drukarnia_api.methods.mixins import MixinWithTagId
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen
class GetTagRelatedAuthors(
    MixinWithTagId,
    BaseMethod[Generator[AuthorModel, None, None]],
):

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[AuthorModel, None, None]:
        response = await session.get(
            url=DrukarniaEndpoints.GetTagRelatedAuthors.format(tag_id=self.tag_id),
            data={},
            **kwargs,
        )

        records = await response.json()
        return (AuthorModel.from_json(record) for record in records)