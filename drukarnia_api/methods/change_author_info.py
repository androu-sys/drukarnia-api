from typing import Any
from attrs import frozen, field
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession
from drukarnia_api.dto import UserInfoUpdate, to_dict


@frozen(kw_only=True)
class ChangeAuthorInfo(BaseMethod[None]):
    config: "UserInfoUpdate"

    url: str = field(
        init=False,
        default="/api/users",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            "PATCH",
            self.url,
            data=to_dict(UserInfoUpdate),
            **kwargs,
        )
