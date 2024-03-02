from typing import Any, TYPE_CHECKING, Generator

from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import NotificationModel
from drukarnia_api.methods.mixins import MixinWithPagination
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetNotifications(
    MixinWithPagination,
    BaseMethod[Generator[NotificationModel, None, None]],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[NotificationModel, None, None]:
        response = await session.get(
            url=DrukarniaEndpoints.GetNotifications,
            data={},
            params={"page": self.page},
            **kwargs,
        )

        data = await response.json()
        return (NotificationModel.from_json(notif) for notif in data)
