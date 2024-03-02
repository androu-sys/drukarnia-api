from typing import Any, TYPE_CHECKING

from attrs import frozen, field, validators
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithCurrentPassword
from drukarnia_api.models import AuthorModel
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class Login(
    MixinWithCurrentPassword,
    BaseMethod[AuthorModel],
):
    email: str = field(
        validator=validators.instance_of(str),
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> AuthorModel:
        # Cookies are automatically updated by aiohttp
        response = await session.post(
            url=DrukarniaEndpoints.AuthorLogin,
            data={
                "password": self.current_password,
                "email": self.email,
            },
            **kwargs,
        )

        author_data = await response.json()
        return AuthorModel.from_json(author_data["user"])
