from warnings import warn
import asyncio
import re

from drukarnia_api.connection import Connection

from typing import Iterable, List, Any, Dict
from datetime import datetime


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

    async def get_followers(self, *args, **kwargs):

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


if __name__ == '__main__':
    author = Author('truman')

    loop = asyncio.get_event_loop()

    loop.run_until_complete(author.login(password='topciz-3haxPo-mezvuz', email='pantry.gene.0y@icloud.com'))

    print(loop.run_until_complete(author.get_notifications()))

