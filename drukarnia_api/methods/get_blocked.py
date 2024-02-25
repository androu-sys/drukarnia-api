from typing import Any, Generator

from attrs import frozen, field

from drukarnia_api.models import AuthorModel
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetBlockedAuthors(BaseMethod[Generator[AuthorModel, None, None]]):
    url: str = field(
        init=False,
        default="/api/relationships/blocked",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[AuthorModel, None, None]:
        response = await session.get(
            self.url,
            data={},
            **kwargs,
        )

        authors = await response.json()
        return (AuthorModel.from_json(author) for author in authors)
