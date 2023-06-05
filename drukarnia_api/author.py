from drukarnia_api.connection import Connection
import asyncio

from typing import Iterable, List, Any
from datetime import datetime


class Author(Connection):
    _id: str = None

    avatar: str = None
    name: str = None
    username: str = None
    description: str = None
    descriptionShort: str = None

    readNum: int = None

    followingNum: int = None
    followingAuthors: List['Author' or dict] = None

    followersNum: int = None
    followersAuthors: List['Author' or dict] = None

    authorTags: List[str] = None
    createdAt: datetime = None
    socials: List[str] = None
    donateUrl: str = None

    articles: List[dict] = None

    relationships: List[Any] = None

    def __init__(self, username: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.username = username

    async def collect_followers(self, return_: bool = False, create_authors: bool = True,
                                *args, **kwargs) -> Iterable['Author']:
        request_url = '/api/relationships/{user_id}/followers?'.format(user_id=self.data['_id'])

        # Make a request to get the followings of the author
        results = await super().search(request_url, *args, **kwargs)

        if create_authors:
            # Create Author objects for each follower and store them in self.followers
            self.followersAuthors = [Author(self.session, data=result) for result in results]

        else:
            self.followersAuthors = results

        if return_:
            return self.followersAuthors

    async def collect_followings(self, return_: bool = False, create_authors: bool = True,
                                 *args, **kwargs) -> Iterable['Author']:
        request_url = '/api/relationships/{user_id}/following?'.format(user_id=self.data['_id'])
        params

        # Make a request to get the followings of the author
        results = await super().search(request_url, *args, **kwargs)

        if create_authors:
            # Create Author objects for each following and store them in self.followings
            self.followingAuthors = [Author(self.session, data=result) for result in results]

        else:
            self.followingAuthors = results

        if return_:
            return self.followingAuthors

    async def get_author_data(self, return_: bool = False) -> dict or None:
        request_url = '/api/users/profile/{username}'.format(username=self.username)

        data = await super().get_json(request_url)

        self.__dict__.update(data)

        if return_:
            return data
