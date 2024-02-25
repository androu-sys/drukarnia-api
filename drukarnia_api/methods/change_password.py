from typing import Any
from attrs import frozen, field
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@frozen
class ChangePassword(BaseMethod[None]):
    old_password: str
    new_password: str
    url: str = field(
        init=False,
        default="/api/users/login/password",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            "PATCH",
            self.url,
            data={
                "oldPassword": self.old_password,
                "newPassword": self.new_password,
            },
            **kwargs,
        )
