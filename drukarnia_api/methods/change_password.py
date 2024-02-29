from typing import Any, TYPE_CHECKING

from attrs import frozen, field, validators
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen
class ChangePassword(BaseMethod[None]):
    old_password: str = field(validator=validators.instance_of(str))
    new_password: str = field(validator=validators.instance_of(str))

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session.patch(
            url=DrukarniaEndpoints.ChangeUserPassword,
            data={
                "oldPassword": self.old_password,
                "newPassword": self.new_password,
            },
            **kwargs,
        )
