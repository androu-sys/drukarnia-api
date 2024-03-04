from typing import TYPE_CHECKING, Any, Iterable

from attrs import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import AuthorModel, SerializedModel, from_json
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetBlockedAuthors(
    BaseMethod[Iterable[AuthorModel]],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Iterable[AuthorModel]:
        response = await session.get(
            url=DrukarniaEndpoints.GetBlockedAuthors,
            data={},
            **kwargs,
        )

        authors_data: Iterable[SerializedModel] = await response.json()
        return (
            from_json(AuthorModel, author)
            for author in authors_data
        )
