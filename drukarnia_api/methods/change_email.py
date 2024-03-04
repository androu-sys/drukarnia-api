from typing import TYPE_CHECKING, Any

from attrs import field, frozen, validators

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithCurrentPassword
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class ChangeEmail(
    MixinWithCurrentPassword,
    BaseMethod[None],
):
    new_email: str = field(validator=validators.instance_of(str))

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        response = await session.patch(
            url=DrukarniaEndpoints.ChangeUserEmail,
            data={
                "currentPassword": self.current_password,
                "newEmail": self.new_email,
            },
            **kwargs,
        )

        data = await response.read()
        success = data.decode("utf-8").lower() == "true"

        if success is False:
            msg = "Email update was not successful."
            raise ValueError(msg)
