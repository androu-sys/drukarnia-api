from typing import Any, TYPE_CHECKING

from attrs import frozen, validators, field
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import AuthorModel
from drukarnia_api.methods.mixins import MixinWithPagination
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetAuthor(MixinWithPagination, BaseMethod[AuthorModel]):
    username: str = field(
        validator=validators.instance_of(str)
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any
    ) -> AuthorModel:
        response = await session.get(
            url=DrukarniaEndpoints.GetAuthorInfo.format(username=self.username),
            data={},
            params={
                "page": self.page
            },
            **kwargs,
        )

        author_data = await response.json()
        return AuthorModel.from_json(author_data)
