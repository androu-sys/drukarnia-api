import re
from typing import Iterable, Any
import asyncio
from aiohttp import ClientSession
from warnings import warn
from .connection import Connection


class Author(Connection):
    def __init__(self, username: str, _id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id

        self.name = None
        self.username = username
        self.description = None
        self.descriptionShort = None

        self.avatar = None

        self.readNum = None
        self.followingNum = None
        self.followersNum = None

        self.authorTags = None
        self.createdAt = None
        self.socials = None
        self.donateUrl = None

        self.articles = None

        self.__authenticated = False

    async def login(self, email: str, password: str):
        data = await self.post_json('/api/users/login',
                                    data={'password': password, 'email': email},
                                    include_header=True)

        data = str(data)

        token = re.search(r'refreshToken=(.*?);', data).group(1)
        device_id = re.search(r'deviceId=(.*?);', data).group(1)

        self.session._default_headers.update({'Cookie': f'deviceId={device_id}; token={token};'})
        self.__authenticated = True

    async def is_authenticated(self):
        if not self.__authenticated:
            raise ValueError('This data requires authentication. Call the login method')

    async def get_followers(self, create_authors: bool = True, offset: int = 0, results_per_page: int = 20,
                            n_collect: int = None, *args, **kwargs) -> Iterable['Author']:
        if self._id is None:
            raise ValueError("User id is a mandatory attribute for followers request. "
                             "Call the collect_data method before using methods that require _id")

        request_url = '/api/relationships/{user_id}/followers'.format(user_id=self._id)

        # Make a request to get the followers of the author
        followers = await self.multi_page_request(request_url, offset, results_per_page, n_collect, *args, **kwargs)

        if create_authors:
            # Create Author objects for each follower and store them in self.followers
            followers = await asyncio.gather(*[
                Author.from_records(self.session, **follower) for follower in followers
            ])

        return followers

    async def get_followings(self, create_authors: bool = True, offset: int = 0, results_per_page: int = 20,
                             n_collect: int = None, *args, **kwargs) -> Iterable['Author']:
        if self._id is None:
            raise ValueError("User id is a mandatory attribute for followings request. "
                             "Call the collect_data method before using methods that require _id")

        request_url = '/api/relationships/{user_id}/following'.format(user_id=self._id)

        # Make a request to get the followings of the author
        followings = await self.multi_page_request(request_url, offset, results_per_page, n_collect, *args, **kwargs)

        if create_authors:
            # Create Author objects for each following and store them in self.followings
            followings = await asyncio.gather(*[
                Author.from_records(self.session, **following) for following in followings
            ])

        return followings

    async def get_notifications(self, offset: int = 0, results_per_page: int = 20,
                                n_collect: int = None, *args, **kwargs) -> Iterable[Any]:
        await self.is_authenticated()

        notifications = await self.multi_page_request('/api/notifications', offset, results_per_page,
                                                      n_collect, *args, **kwargs)

        return notifications

    async def get_reads_history(self, offset: int = 0, results_per_page: int = 20,
                                n_collect: int = None, *args, **kwargs) -> Iterable[Any]:
        await self.is_authenticated()

        reads_history = await self.multi_page_request('/api/stats/reads/history', offset, results_per_page,
                                                      n_collect, *args, **kwargs)

        return reads_history

    async def get_sections(self, preview: bool = True, *args, **kwargs) -> Iterable[Any]:
        await self.is_authenticated()

        sections = await self.get_json(f'/api/articles/bookmarks/lists?preview={str(preview).lower()}',
                                       *args, **kwargs)

        return sections

    async def collect_data(self, return_: bool = False) -> dict or None:
        request_url = '/api/users/profile/{username}'.format(username=self.username)

        data = await super().get_json(request_url)
        if not data:
            warn('No new data was found')

        self.__dict__ = {key: data.get(key, value)
                         for key, value in self.__dict__.items()}

        if return_:
            return data

    @staticmethod
    async def from_records(session: ClientSession, username: str, **kwargs) -> 'Author':
        new_author = Author(username=username, session=session)
        new_author.__dict__ = {key: kwargs.get(key, value)
                               for key, value in new_author.__dict__.items()}

        return new_author

    def __hash__(self):
        return hash(self._id or self.username)
