from typing import TYPE_CHECKING, Any, Iterable

from attrs import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithPagination, MixinWithQuery
from drukarnia_api.models import ArticleModel, SerializedModel, from_json
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class FindArticle(    # type: ignore[misc]
    MixinWithPagination,
    MixinWithQuery,
    BaseMethod[Iterable[ArticleModel]],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Iterable[ArticleModel]:
        response = await session.get(
            url=DrukarniaEndpoints.FindArticles,
            data={},
            params={
                "name": self.query,
                "page": self.page,
            },
            **kwargs,
        )

        records: Iterable[SerializedModel] = await response.json()
        return (
            from_json(ArticleModel, record)
            for record in records
        )
