from typing import Any
from attrs import frozen
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.subscribe import Subscribe
from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class Unsubscribe(Subscribe, BaseMethod[None]):
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
