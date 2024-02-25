from typing import Any
from attrs import field, frozen, validators
from drukarnia_api.models import AuthorModel
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPage
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetAuthor(BaseMethod[AuthorModel]):
    username: str = field(validator=validators.instance_of(str))
    url: str = field(init=False, default="/api/users/profile/{username}")

    async def _request(
        self, session: "DrukarniaSession", **kwargs: Any
    ) -> AuthorModel:
        response = await session.get(
            self.url.format(username=self.username),
            data={},
            params={
                "page": self.page
            },
            **kwargs,
        )

        author_data = await response.json()
        return AuthorModel.from_json(author_data)
