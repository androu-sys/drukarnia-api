from typing import Any, Generator
from drukarnia_api.objects.author import Author
from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.network.session import DrukarniaSession
from attrs import define, field, validators


@define
class GetFollowers(BaseMethod[Generator[Author, None, None]]):
    author: "Author"

    page: int = field(
        default=0,
        validator=(
            validators.instance_of(int),
            validators.ge(0)
        ),
    )
    # Default and unchangeable constant in current Drukarnia-API. Use it to standardize your code.
    page_size: int = field(init=False, default=20)
    url: str = field(init=False, default="/api/relationships/{author_id}/followers")

    async def _from_response(
        self,
        session: "DrukarniaSession",
        *args: Any,
        **kwargs: Any
    ) -> Generator[Author, None, None]:
        authors = await session.get(
            self.url.format(author_id=self.author.author_id),
            data={},
            params={
                "page": self.page
            },
        )

        return (Author(**author) for author in authors)
