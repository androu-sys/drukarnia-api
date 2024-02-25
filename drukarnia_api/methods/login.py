from typing import Any

from attr import define, field, validators
from drukarnia_api.models import AuthorModel
from drukarnia_api.methods import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@define(frozen=True)
class Login(BaseMethod[AuthorModel]):
    email: str = field(validator=validators.instance_of(str))
    password: str = field(validator=validators.instance_of(str))

    url: str = field(
        init=False,
        default="'/api/users/login",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> AuthorModel:
        # Cookies are automatically updated by aiohttp
        response = await session.post(
            data={"password": self.password, "email": self.email},
            **kwargs,
        )

        author_data = await response.json()
        return AuthorModel(**author_data["user"])
