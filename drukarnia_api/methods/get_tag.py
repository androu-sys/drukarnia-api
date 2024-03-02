from typing import Any, TYPE_CHECKING, Generator

from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import TagModel
from drukarnia_api.methods.mixins import MixinWithTagSlug
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetTag(
    MixinWithTagSlug,
    BaseMethod[Generator[TagModel, None, None]],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[TagModel, None, None]:
        response = await session.get(
            url=DrukarniaEndpoints.GetTag.format(tag_slug=self.tag_slug),
            data={},
            params={
                # Drukarnia uses pagination for this request.
                # Although it returns information ONLY for the first one :/
                "page": 1,
            },
            **kwargs,
        )

        records = await response.json()
        return (TagModel.from_json(record) for record in records)
