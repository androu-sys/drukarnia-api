from warnings import warn
import asyncio
import re

from drukarnia_api.connection import Connection


from typing import Iterable, Any
from aiohttp import ClientSession


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

    async def login(self, password: str, email: str):
        data = await self.post_json('/api/users/login',
                                    data={'password': password, 'email': email},
                                    include_header=True)

        data = str(data)

        token = re.search(r'refreshToken=(.*?);', data).group(1)
        device_id = re.search(r'deviceId=(.*?);', data).group(1)

        self.session._default_headers.update({'Cookie': f'deviceId={device_id}; token={token};'})
        self.__authenticated = True

    async def get_followers(self, *args, **kwargs) -> Iterable['Author']:
        if self._id is None:
            raise ValueError("User id is a mandatory attribute for followers scrapper. "
                             "Call collect_data method before using _id required methods")

        request_url = '/api/relationships/{user_id}/followers'.format(user_id=self._id)

        def synthesizer(url):
            start_page = 1

            while True:
                yield {'url': url, 'params': {'page': start_page}}
                start_page += 1

        # Make a request to get the followings of the author
        followers = await super().run_until_no_stop(synthesizer(request_url), lambda r: r != [], *args, **kwargs)

        # Create Author objects for each follower and store them in self.followers
        return await asyncio.gather(*[Author.from_records(self.session, **follower[0]) for follower in followers])

    async def get_followings(self, *args, **kwargs) -> Iterable['Author']:
        if self._id is None:
            raise ValueError("User id is a mandatory attribute for followers scrapper. "
                             "Call collect_data method before using _id required methods")

        request_url = '/api/relationships/{user_id}/followings'.format(user_id=self._id)

        def synthesizer(url):
            start_page = 1

            while True:
                yield {'url': url, 'params': {'page': start_page}}
                start_page += 1

        # Make a request to get the followings of the author
        followings = await super().run_until_no_stop(synthesizer(request_url), lambda r: r != [], *args, **kwargs)

        # Create Author objects for each follower and store them in self.followers
        return await asyncio.gather(*[Author.from_records(self.session, **following[0]) for following in followings])

    async def get_notifications(self, *args, **kwargs) -> Iterable[Any]:
        request_url = '/api/notifications'

        def synthesizer(url):
            start_page = 1

            while True:
                yield {'url': url, 'params': {'page': start_page}}
                start_page += 1

        notifications = await self.run_until_no_stop(synthesizer(request_url),
                                                     lambda r: r != [],
                                                     *args, **kwargs)

        return notifications

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


if __name__ == '__main__':
    author = Author('truman')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(author.collect_data())

    followings = loop.run_until_complete(author.get_followings())
    print(len(followings))

    print(followings[0].name)

