from typing import Any, Generator

from attr import field, frozen, validators

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import TagSummaryModel
from drukarnia_api.network.session import DrukarniaSession

from drukarnia_api.methods.mixins import MixinWithPage


@frozen(kw_only=True)
class GetRelatedTags(MixinWithPage, BaseMethod[Generator[TagSummaryModel, None, None]]):
    tag_id: str = field(validator=validators.instance_of(str))
    url: str = field(init=False, default="/api/articles/tags/{tag_id}/related")

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[TagSummaryModel, None, None]:
        response = await session.get(
            url=self.url.format(tag_id=self.tag_id),
            data={},
            params={"page": self.page},
            **kwargs,
        )

        data = await response.json()
        return (TagSummaryModel.from_json(**record) for record in data)
