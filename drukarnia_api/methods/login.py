from typing import Any

from attr import define, field
import re
from drukarnia_api.methods import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@define(frozen=True)
class Login(BaseMethod[None]):
    email: str
    password: str

    url: str = field(
        init=False,
        default="'/api/users/login",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        await session.post(
            data={"password": self.password, "email": self.email},
            *args,
            **kwargs,
        )
