from typing import Any, TYPE_CHECKING

from attr import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.dto import UserInfoUpdate
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen
class ChangeAuthorInfo(BaseMethod[None]):
    config: "UserInfoUpdate"

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session.patch(
            DrukarniaEndpoints.ChangeUserGeneralInfo,
            data=self.config.as_dict(),
            **kwargs,
        )
