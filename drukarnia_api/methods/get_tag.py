from typing import TYPE_CHECKING, Any

from attrs import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithTagSlug
from drukarnia_api.models import SerializedModel, TagModel, from_json
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetTag(
    MixinWithTagSlug,
    BaseMethod[TagModel],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> TagModel:
        response = await session.get(
            url=DrukarniaEndpoints.GetTag.format(tag_slug=self.tag_slug),    # type: ignore[str-format]
            data={},
            params={
                # Drukarnia uses pagination for this request.
                # Although it returns information ONLY for the first one :/
                "page": 1,
            },
            **kwargs,
        )

        record: SerializedModel = await response.json()
        return from_json(TagModel, record)
