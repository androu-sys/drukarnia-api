from typing import Optional
from datetime import datetime
from attr import define, field, validators
from drukarnia_api.network.utils import _to_datetime


@define
class Relationship:
    isSubscribed: bool = field(validator=validators.instance_of(bool))
    isBlocked: bool = field(validator=validators.instance_of(bool))


@define
class Author:
    id: str = field(
        validator=validators.instance_of(str),
    )
    name: str = field(
        validator=validators.instance_of(str),
    )
    avatar: Optional[str] = field(
        validator=validators.instance_of(str | type(None)),
    )
    username: str = field(validator=validators.instance_of(str))
    description: Optional[str] = field(
        validator=validators.instance_of(str | type(None))
    )
    followingNum: int = field(
        validator=(validators.instance_of(int), validators.ge(val=0))
    )
    followersNum: int = field(
        validator=validators.instance_of(int),
    )
    readNum: int = field(
        validator=(validators.instance_of(int), validators.ge(val=0)),
    )
    authorTags: list = field(
        validator=validators.instance_of(list),
    )
    createdAt: str = field(
        validator=validators.instance_of(datetime),
        converter=_to_datetime,
    )
    relationships: Relationship = field(
        converter=lambda _dict: Relationship(**_dict),
    )
    articles: list = field(
        validator=validators.instance_of(list),
    )


async def get_author_article_titles():
    from drukarnia_api.network.api import API
    from drukarnia_api.methods import GetFollowers

    api = API()
    d = {'username': 'mantis', 'id': '64540062c149c83ef72eea62', 'name': 'Ляшенко Ізабелла', 'avatar': None,
         'description': None, 'followingNum': 0, 'followersNum': 0, 'readNum': 0, 'authorTags': [],
         'createdAt': '2023-05-04T18:58:42.868Z', 'relationships': {'isSubscribed': False, 'isBlocked': False},
         'articles': []}

    async with api:
        gen = await api(GetFollowers(author=Author(**d)))

        for authro in gen:
            print(authro)


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_author_article_titles())
