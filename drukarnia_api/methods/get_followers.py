from typing import Any, Generator

from attrs import define, field

from drukarnia_api.dto.author import Author
from drukarnia_api.methods.base import BaseMethod, ResponseBase
from drukarnia_api.methods.mixins import MixinWithPage
from drukarnia_api.network.session import DrukarniaSession


@define(frozen=True)
class GetFollowers(MixinWithPage, BaseMethod[Generator[Author, None, None]]):

    author_id: str  # type: ignore[misc]
    url: str = field(init=False, default="/api/relationships/{author_id}/followers")

    async def _request(
        self, session: "DrukarniaSession", *args: Any, **kwargs: Any
    ) -> Generator[Author, None, None]:
        response = await session.get(
            self.url.format(author_id=self.author_id),
            data={},
            params={
                "page": self.page
            },
            *args,
            **kwargs,
        )

        authors = await response.json()
        return (Author(**author) for author in authors)
