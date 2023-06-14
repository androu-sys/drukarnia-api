import re
from typing import Iterable, Any
import asyncio

from aiohttp import ClientSession
from drukarnia_api.connection.connection import Connection
from inspect import currentframe


class Author(Connection):
    def __init__(self, username: str = None, _id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id
        self.username = username
        self.name = None
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

    async def login(self, email: str, password: str) -> None:
        """
        Log in the author with the provided email and password.
        """

        data = await self.post('/api/users/login',
                               data={'password': password, 'email': email},
                               output='headers')

        data = str(data)

        token = re.search(r'refreshToken=(.*?);', data).group(1)
        device_id = re.search(r'deviceId=(.*?);', data).group(1)

        self.session.headers.update({'Cookie': f'deviceId={device_id}; token={token};'})

    async def control_params(self, *args) -> None:
        """
        Validate the required fields for processing a specific method.
        """

        calling_by = currentframe().f_back.f_code.co_name

        for name in args:
            if not self.__dict__.get(name, None):
                raise ValueError(f'field {name} is required to process {calling_by}. Usually required data can be'
                                 f'obtained by calling collect_data method first.')

    async def get_followers(self, create_authors: bool = True, offset: int = 0, results_per_page: int = 20,
                            n_collect: int = None, *args, **kwargs) -> Iterable['Author']:
        """
        Get the followers of the author.
        """

        await self.control_params('_id')

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
        """
        Get the followings of the author.
        """

        await self.control_params('_id')

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
                                n_collect: int = None, *args, **kwargs) -> Iterable[list or dict]:
        """
        Get the notifications of the author.
        """

        await self.is_authenticated()

        notifications = await self.multi_page_request('/api/notifications', offset, results_per_page,
                                                      n_collect, *args, **kwargs)

        return notifications

    async def get_reads_history(self, offset: int = 0, results_per_page: int = 20,
                                n_collect: int = None, *args, **kwargs) -> Iterable[list or dict]:
        """
        Get the reading history of the author.
        """

        await self.is_authenticated()

        reads_history = await self.multi_page_request('/api/stats/reads/history', offset, results_per_page,
                                                      n_collect, *args, **kwargs)

        return reads_history

    async def get_sections(self, preview: bool = True, *args, **kwargs) -> Iterable[list or dict]:
        """
        Get the sections of the author's articles.
        """
        await self.is_authenticated()

        sections = await self.get(f'/api/articles/bookmarks/lists?preview={str(preview).lower()}',
                                  output='json', *args, **kwargs)

        return sections

    async def create_section(self, name: str, **kwargs) -> Any:
        """
        Create a new section for the author's articles.
        """

        await self.is_authenticated()

        return await self.post('/api/articles/bookmarks/lists', data={"name": name}, output='read', **kwargs)

    async def delete_section(self, section_id: str, **kwargs) -> Any:
        """
        Delete a section for the author's articles.
        """

        await self.is_authenticated()

        return await self.delete(f'/api/articles/bookmarks/lists/{section_id}', **kwargs)

    async def get_blocked(self) -> Iterable[list or dict]:
        """
        Get the authors blocked by the current author.
        """

        await self.is_authenticated()

        return await self.get('/api/relationships/blocked')

    async def username_exists(self, username: str) -> bool:
        """
        Check if the given username exists.
        """

        return bool(await self.get('/api/users/username', params={'username': username}, output='read'))

    async def change_password(self, old_password: str, new_password: str, **kwargs) -> Any:
        """
        Change the author's password.
        """

        await self.is_authenticated()

        return await self.patch(f'/api/users/login/password',
                                data={"oldPassword": old_password,
                                      "newPassword": new_password},
                                **kwargs)

    async def change_user_info(self, name: str = None, description: str = None, username: str = None,
                               description_short: str = None, socials: dict = None, donate_url: str = None) -> None:
        """
        Change the author's user information.
        """

        await self.is_authenticated()

        data = {"name": name, "description": description, "username": username,
                "descriptionShort": description_short,
                "socials": socials, "donateUrl": donate_url}
        data = {key: value for key, value in data.items() if value is not None}

        await self.patch('/api/users', data=data, output=[])

    async def change_email(self, current_password: str, new_email: str, **kwargs) -> Any:
        """
        Change the author's email.
        """

        await self.is_authenticated()

        return await self.patch(f'/api/users/login/email',
                                data={"currentPassword": current_password,
                                      "newEmail": new_email},
                                **kwargs)

    async def collect_data(self, return_: bool = False) -> dict or None:
        """
        Collect the author's data and update the object's attributes.
        """

        await self.control_params('username')

        request_url = '/api/users/profile/{username}'.format(username=self.username)

        data = await self.get(request_url, output='json')
        self.__dict__ = {key: data.get(key, value)
                         for key, value in self.__dict__.items()}

        if return_:
            return data

    @staticmethod
    async def from_records(session: ClientSession, **kwargs) -> 'Author':
        """
        Create an Author instance from records.
        """

        new_author = Author(session=session)
        new_author.__dict__ = {key: kwargs.get(key, value)
                               for key, value in new_author.__dict__.items()}

        return new_author

    def __hash__(self):
        return hash(self._id or self.username)
