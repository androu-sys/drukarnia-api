from typing import Any
from attrs import frozen, field, asdict
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession
from drukarnia_api.dto.socials import Socials


@frozen
class ChangUserInfoConfig:
    name: str = None
    description: str = None
    username: str = None
    description_short: str = None
    socials: Socials = None
    donate_url: str = None


@frozen(kw_only=True)
class ChangeAuthorInfo(BaseMethod[None]):
    config: "ChangUserInfoConfig"

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
            data=asdict(self.config),
            **kwargs,
        )
