from typing import Any

from attr import define, field, validators
from drukarnia_api.methods import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@define(frozen=True)
class Login(BaseMethod[None]):
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
    ) -> None:
        # Cookies are automatically updated by aiohttp
        await session.post(
            data={"password": self.password, "email": self.email},
            **kwargs,
        )
