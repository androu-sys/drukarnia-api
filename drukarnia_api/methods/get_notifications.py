from typing import TYPE_CHECKING, Any, Iterable

from attrs import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPagination
from drukarnia_api.models import NotificationModel, SerializedModel, from_json
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetNotifications(
    MixinWithPagination,
    BaseMethod[Iterable[NotificationModel]],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Iterable[NotificationModel]:
        response = await session.get(
            url=DrukarniaEndpoints.GetNotifications,
            data={},
            params={"page": self.page},
            **kwargs,
        )

        data: Iterable[SerializedModel] = await response.json()
        return (
            from_json(NotificationModel, notif)
            for notif in data
        )
