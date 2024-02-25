from typing import Any, Generator

from attr import field, frozen, validators

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.models import ExtendedCardArticleModel
from drukarnia_api.network.session import DrukarniaSession

from drukarnia_api.methods.mixins import MixinWithPage


@frozen(kw_only=True)
class GetArticlesFromTag(MixinWithPage, BaseMethod[Generator[ExtendedCardArticleModel, None, None]]):
    tag_slug: str = field(validator=validators.instance_of(str))
    url: str = field(init=False, default="/api/articles/tags/{tag_slug}")

    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> Generator[ExtendedCardArticleModel, None, None]:
        response = await session.get(
            url=self.url.format(tag_slug=self.tag_slug),
            data={},
            params={"page": self.page},
            **kwargs,
        )

        data = (await response.json())["articles"]
        return (ExtendedCardArticleModel.from_json(**record) for record in data)
