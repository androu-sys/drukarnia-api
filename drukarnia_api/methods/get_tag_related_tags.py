from typing import Any, TYPE_CHECKING, Generator

from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import TagModel
from drukarnia_api.methods.mixins import MixinWithTagId, MixinWithPagination
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetTagRelatedTags(
    MixinWithTagId,
    MixinWithPagination,
    BaseMethod[Generator[TagModel, None, None]],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[TagModel, None, None]:
        response = await session.get(
            url=DrukarniaEndpoints.GetTagRelatedTags.format(tag_id=self.tag_id),
            data={},
            params={
                "page": self.page,
            },
            **kwargs,
        )

        records = await response.json()
        return (TagModel.from_json(record) for record in records)
