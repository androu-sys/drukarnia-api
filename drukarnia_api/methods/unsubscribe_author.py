from typing import Any
from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.subscribe_author import SubscribeAuthor
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class UnsubscribeAuthor(SubscribeAuthor, BaseMethod[None]):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        await session(
            "DELETE",
            self.url.format(author_id=self.author_id),
            data={},
            **kwargs,
        )
