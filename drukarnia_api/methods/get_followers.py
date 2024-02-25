from typing import Any, Generator
from attrs import field, frozen, validators
from drukarnia_api.models import AuthorModel
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPage
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetFollowers(MixinWithPage, BaseMethod[Generator[AuthorModel, None, None]]):
    author_id: str = field(validator=validators.instance_of(str))
    url: str = field(init=False, default="/api/relationships/{author_id}/followers")

    async def _request(
        self, session: "DrukarniaSession", **kwargs: Any
    ) -> Generator[AuthorModel, None, None]:
        response = await session.get(
            self.url.format(author_id=self.author_id),
            data={},
            params={
                "page": self.page
            },
            **kwargs,
        )

        authors = await response.json()
        return (AuthorModel(**author) for author in authors)
