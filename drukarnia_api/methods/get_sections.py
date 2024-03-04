from typing import TYPE_CHECKING, Any, Iterable

from attrs import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPreviewOption
from drukarnia_api.models import SectionModel, SerializedModel, from_json
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class GetSections(
    MixinWithPreviewOption,
    BaseMethod[Iterable[SectionModel]],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Iterable[SectionModel]:
        response = await session.get(
            url=DrukarniaEndpoints.GetSections,
            data={},
            params={
                "preview": self.preview,
            },
            **kwargs,
        )

        articles: Iterable[SerializedModel] = await response.json()
        return (
            from_json(SectionModel, article)
            for article in articles
        )
