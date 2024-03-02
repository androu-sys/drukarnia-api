from typing import Any, TYPE_CHECKING

from attrs import frozen, field, validators
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithSectionName
from drukarnia_api.models import SectionModel
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class CreateSection(
    MixinWithSectionName,
    BaseMethod[SectionModel],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> SectionModel:
        response = await session.get(
            url=DrukarniaEndpoints.CreateNewSection,
            data={},
            params={
                "name": self.section_name,
            },
            **kwargs,
        )

        section_id = await response.read()
        return SectionModel(
            id_=section_id.decode('utf-8'),
            name=self.name,
        )
