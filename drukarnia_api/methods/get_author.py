from typing import Any, TYPE_CHECKING

from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import AuthorModel
from drukarnia_api.methods.mixins import MixinWithUsername
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetAuthor(
    MixinWithUsername,
    BaseMethod[AuthorModel],
):

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any
    ) -> AuthorModel:
        response = await session.get(
            url=DrukarniaEndpoints.GetAuthorInfo.format(username=self.username),
            data={},
            **kwargs,
        )

        author_data = await response.json()
        return AuthorModel.from_json(author_data)   # type: ignore[no-any-return]
