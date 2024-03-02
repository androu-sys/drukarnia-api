from typing import Any, TYPE_CHECKING, Generator

from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import AuthorModel
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetBlockedAuthors(
    BaseMethod[Generator[AuthorModel, None, None]],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[AuthorModel, None, None]:
        response = await session.get(
            url=DrukarniaEndpoints.GetBlockedAuthors,
            data={},
            **kwargs,
        )

        authors_data = await response.json()
        return (AuthorModel.from_json(author) for author in authors_data)
