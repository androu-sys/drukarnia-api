from attrs import frozen, field
from typing import TYPE_CHECKING, Any, Iterable

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithAuthorId, MixinWithPagination
from drukarnia_api.models import AuthorModel, SerializedModel, from_json
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetFollowers(
    MixinWithPagination,
    MixinWithAuthorId,
    BaseMethod[Iterable[AuthorModel]],
):
    url: str = field(
        init=False,
        default=DrukarniaEndpoints.GetFollowers,
    )

    async def _request(
        self, session: "DrukarniaSession", **kwargs: Any,
    ) -> Iterable[AuthorModel]:
        response = await session.get(
            url=self.url.format(author_id=self.author_id),
            data={},
            params={
                "page": self.page,
            },
            **kwargs,
        )

        authors: Iterable[SerializedModel] = await response.json()
        return (
            from_json(AuthorModel, author)
            for author in authors
        )
