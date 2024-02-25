from typing import Generator
from drukarnia_api.dto.author import Author
from drukarnia_api.methods.get_followers import GetFollowers
from attrs import define, field


@define
class GetFollowings(GetFollowers[Generator[Author, None, None]]):
    url: str = field(
        init=False,
        default="/api/relationships/{author_id}/following",
    )
