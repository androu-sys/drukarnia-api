from typing import TYPE_CHECKING, Any, Iterable

from attrs import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPagination, MixinWithTagId
from drukarnia_api.models import SerializedModel, TagModel, from_json
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetTagRelatedTags(
    MixinWithTagId,
    MixinWithPagination,
    BaseMethod[Iterable[TagModel]],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Iterable[TagModel]:
        response = await session.get(
            url=DrukarniaEndpoints.GetTagRelatedTags.format(tag_id=self.tag_id),    # type: ignore[str-format]
            data={},
            params={
                "page": self.page,
            },
            **kwargs,
        )

        records: Iterable[SerializedModel] = await response.json()
        return (
            from_json(TagModel, record)
            for record in records
        )
