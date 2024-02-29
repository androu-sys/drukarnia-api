from typing import Any, TYPE_CHECKING, Generator

from attrs import frozen, field, validators
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import AuthorModel
from drukarnia_api.methods.mixins import MixinWithPagination, MixinWithQuery
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class FindAuthor(MixinWithPagination, MixinWithQuery, BaseMethod[Generator[AuthorModel, None, None]]):
    with_relations: bool = field(
        validator=validators.instance_of(bool),
        default=False,
    )

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[AuthorModel, None, None]:
        response = await session.get(
            url=DrukarniaEndpoints.FindAuthors,
            data={},
            params={
                "name": self.query,
                "withRelationships": self.with_relations,
                "page": self.pge,
            },
            **kwargs,
        )

        records = await response.json()
        return (AuthorModel.from_json(record) for record in records)
