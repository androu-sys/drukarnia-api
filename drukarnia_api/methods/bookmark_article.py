from typing import Any, TYPE_CHECKING

from attr import frozen

from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.mixins import MixinWithArticleId, MixinWithSectionId, MixinWithUnbookmarkOption
from drukarnia_api.network.endpoints import DrukarniaEndpoints

if TYPE_CHECKING:
    from drukarnia_api.network.session import DrukarniaSession


@frozen(kw_only=True)
class BookmarkArticle(
    MixinWithArticleId,
    MixinWithSectionId,
    MixinWithUnbookmarkOption,
    BaseMethod[None],
):
    async def _request(
        self,
        session: "DrukarniaSession",
        **kwargs: Any,
    ) -> None:
        if self.unbookmark:
            await session.delete(
                url=DrukarniaEndpoints.UnBookmarkArticle.format(article_id=self.article_id),
                data={},
                **kwargs,
            )
            return

        await session.post(
            url=DrukarniaEndpoints.BookmarkArticle,
            data={
                "article": self.article_id,
                "list": self.section_id,
            },
            **kwargs,
        )
