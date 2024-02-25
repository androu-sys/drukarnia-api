from typing import Any, Generator

from attr import define, field

from drukarnia_api.dto import Author
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPage
from drukarnia_api.network.session import DrukarniaSession


@define(frozen=True)
class GetNotifications(MixinWithPage, BaseMethod[Generator[Author, None, None]]):
    url: str = field(
        init=False,
        default="/api/notifications",
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        *args: Any,
        **kwargs: Any,
    ) -> Generator[Author, None, None]:
        response = await session.get(
            data={},
            params={"page": self.page},
            *args,
            **kwargs,
        )

        authors = await response.json()
        return (Author(**author) for author in authors)  # Change the model from Author to Notification 
