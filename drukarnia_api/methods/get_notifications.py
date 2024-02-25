from typing import Any, Generator

from attrs import frozen, field

from drukarnia_api.models import NotificationModel
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPage
from drukarnia_api.network.session import DrukarniaSession


@frozen
class GetNotifications(MixinWithPage, BaseMethod[Generator[NotificationModel, None, None]]):
    url: str = field(
        init=False,
        default="/api/notifications",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[NotificationModel, None, None]:
        response = await session.get(
            data={},
            params={"page": self.page},
            **kwargs,
        )

        notifications = await response.json()
        return (NotificationModel(**author) for author in notifications)
