from typing import Any
from attrs import frozen, field
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession


@frozen
class ChangeEmail(BaseMethod[None]):
    current_password: str
    new_email: str

    url: str = field(
        init=False,
        default="/api/users/login/email",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        response = await session(
            "PATCH",
            self.url,
            data={
                "currentPassword": self.current_password,
                "newEmail": self.new_email,
            },
            **kwargs,
        )

        data = await response.read()
        success = data.decode('utf-8').lower() == "true"

        if success is False:
            raise ValueError("Email update was not successful. We have no idea why.")
