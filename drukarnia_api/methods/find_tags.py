from typing import TYPE_CHECKING, Any, Iterable

from attrs import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPagination, MixinWithQuery
from drukarnia_api.models import SerializedModel, TagModel, from_json
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class FindTags(    # type: ignore[misc]
    MixinWithPagination,
    MixinWithQuery,
    BaseMethod[Iterable[TagModel]],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Iterable[TagModel]:
        response = await session.get(
            url=DrukarniaEndpoints.FindTags,
            data={},
            params={
                "text": self.query,
                "page": self.page,
            },
            **kwargs,
        )

        records: Iterable[SerializedModel] = (await response.json())["tags"]
        return (
            from_json(TagModel, record)
            for record in records
        )
