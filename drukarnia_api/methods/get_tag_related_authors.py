from typing import TYPE_CHECKING, Any, Iterable

from attrs import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithTagId
from drukarnia_api.models import AuthorModel, SerializedModel, from_json
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetTagRelatedAuthors(
    MixinWithTagId,
    BaseMethod[Iterable[AuthorModel]],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Iterable[AuthorModel]:
        response = await session.get(
            url=DrukarniaEndpoints.GetTagRelatedAuthors.format(tag_id=self.tag_id),    # type: ignore[str-format]
            data={},
            **kwargs,
        )

        records: Iterable[SerializedModel] = await response.json()
        return (
            from_json(AuthorModel, record)
            for record in records
        )
