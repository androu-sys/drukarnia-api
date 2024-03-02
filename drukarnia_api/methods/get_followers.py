from typing import Any, TYPE_CHECKING, Generator

from attrs import frozen, field
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import AuthorModel
from drukarnia_api.methods.mixins import MixinWithPagination, MixinWithAuthorId
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetFollowers(
    MixinWithPagination,
    MixinWithAuthorId,
    BaseMethod[Generator[AuthorModel, None, None]],
):
    url: str = field(
        init=False,
        default=DrukarniaEndpoints.GetFollowers
    )

    async def _request(
        self, session: "DrukarniaSession", **kwargs: Any
    ) -> Generator[AuthorModel, None, None]:
        response = await session.get(
            url=self.url.format(author_id=self.author_id),
            data={},
            params={
                "page": self.page
            },
            **kwargs,
        )

        authors = await response.json()
        return (AuthorModel.from_json(author) for author in authors)
