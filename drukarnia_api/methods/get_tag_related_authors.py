from typing import Any, Generator

from attr import field, frozen, validators

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import TagRelatedAuthorsModel
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetRelatedAuthorsFromTag(BaseMethod[Generator[TagRelatedAuthorsModel, None, None]]):
    tag_id: str = field(validator=validators.instance_of(str))
    url: str = field(init=False, default="/api/users/tags/{tag_id}/related")

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[TagRelatedAuthorsModel, None, None]:
        response = await session.get(
            url=self.url.format(tag_id=self.tag_id),
            data={},
            **kwargs,
        )

        data = await response.json()
        return (TagRelatedAuthorsModel.from_json(**record) for record in data)
