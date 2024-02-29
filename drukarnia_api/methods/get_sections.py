from typing import Any, TYPE_CHECKING, Generator

from attrs import frozen, field, validators
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import SectionModel
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetSections(BaseMethod[Generator[SectionModel, None, None]]):
    preview: bool = field(
        validator=validators.instance_of(bool),
        default=False
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[SectionModel, None, None]:
        response = await session.get(
            url=DrukarniaEndpoints.GetSections,
            data={},
            params={
                "preview": self.preview,
            },
            **kwargs,
        )

        articles = await response.json()
        return (SectionModel.from_json(article) for article in articles)
