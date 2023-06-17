import re
from typing import Iterable, Any
import asyncio
from warnings import warn

from aiohttp import ClientSession
from drukarnia_api.connection.connection import Connection


class Author(Connection):
    def __init__(self, username: str = None, _id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.author_data: dict = {'username': username, '_id': _id}

    async def login(self, email: str, password: str) -> None:
        """
        Log in the author with the provided email and password.
        """

        headers, info = await self.post('/api/users/login',
                                        data={'password': password, 'email': email},
                                        output=['headers', 'json'])

        if self.author_id and (self.author_id != info['user']['_id']):
            raise ValueError('You try to log into unrelated author')

        elif self.username and (self.username != info['user']['username']):
            raise ValueError('You try to log into unrelated author')

        elif not (self.author_id or self.username):
            warn("We weren't able to indentify any relationship between current Author data and the Druakrnia "
                 "User you are trying to log into. It may cause unexpected and fatal errors. Please consider "
                 "initializing Author class with username or _id. Alternatively run collect_data method before!")

        headers = str(headers)

        token = re.search(r'refreshToken=(.*?);', headers).group(1)
        device_id = re.search(r'deviceId=(.*?);', headers).group(1)

        self.session.headers.update({'Cookie': f'deviceId={device_id}; token={token};'})

    async def _control_attr(self, attr: str) -> None:
        if getattr(self, attr) is None:
            raise ValueError(f'{attr} is required. If you don\'t now it, call collect_data method before')

    async def get_followers(self, create_authors: bool = True, offset: int = 0, results_per_page: int = 20,
                            n_collect: int = None, *args, **kwargs) -> Iterable['Author']:
        """
        Get the followers of the author.
        """
        await self._control_attr('author_id')

        request_url = '/api/relationships/{user_id}/followers'.format(user_id=self.author_id)

        # Make a request to get the followers of the author
        followers = await self.multi_page_request(request_url, offset, results_per_page, n_collect, *args, **kwargs)

        if create_authors:
            # Create Author objects for each follower and store them in self.followers
            followers = await asyncio.gather(*[
                Author.from_records(self.session, follower_data) for follower_data in followers
            ])

        return followers

    async def get_followings(self, create_authors: bool = True, offset: int = 0, results_per_page: int = 20,
                             n_collect: int = None, *args, **kwargs) -> Iterable['Author']:
        """
        Get the followings of the author.
        """

        await self._control_attr('author_id')

        request_url = '/api/relationships/{user_id}/following'.format(user_id=self.author_id)

        # Make a request to get the followings of the author
        followings = await self.multi_page_request(request_url, offset, results_per_page, n_collect, *args, **kwargs)

        if create_authors:
            # Create Author objects for each following and store them in self.followings
            followings = await asyncio.gather(*[
                Author.from_records(self.session, following_data) for following_data in followings
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

    async def subscribe(self, author_id: str, unsubscribe: bool = False) -> None:
        await self.is_authenticated()

        request_url = f'/api/relationships/subscribe/{author_id}'

        if unsubscribe:
            await self.delete(request_url)
            return None

        await self.post(request_url)

    async def block(self, author_id: str, unblock: bool = False) -> None:
        await self.is_authenticated()

        request_url = f'/api/relationships/block/{author_id}'

        if unblock:
            await self.patch(request_url)
            return None

        await self.put(request_url)

    async def get_blocked(self) -> Iterable[list or dict]:
        """
        Get the authors blocked by the current author.
        """

        await self.is_authenticated()

        return await self.get('/api/relationships/blocked')

    async def change_password(self, old_password: str, new_password: str, **kwargs) -> str:
        """
        Change the author's password.
        """

        await self.is_authenticated()

        response = await self.patch(f'/api/users/login/password',
                                    data={"oldPassword": old_password, "newPassword": new_password},
                                    output='read',
                                    **kwargs)

        return response

    async def change_user_info(self, name: str = None, description: str = None, username: str = None,
                               description_short: str = None, socials: dict = None, donate_url: str = None) -> str:
        """
        Change the author's user information.
        """

        await self.is_authenticated()

        info2patch = {"name": name, "description": description, "username": username,
                      "descriptionShort": description_short,
                      "socials": socials, "donateUrl": donate_url}

        info2patch = {key: value for key, value in info2patch.items() if value is not None}

        response = await self.patch('/api/users', data=info2patch, output='read')
        return response

    async def change_email(self, current_password: str, new_email: str, **kwargs) -> str:
        """
        Change the author's email.
        """

        await self.is_authenticated()

        response = await self.patch(f'/api/users/login/email',
                                    data={"currentPassword": current_password, "newEmail": new_email},
                                    output='read',
                                    **kwargs)

        return response

    async def collect_data(self, return_: bool = False) -> dict or None:
        """
        Collect the author's data and update the object's attributes.
        """

        await self._control_attr('username')

        request_url = '/api/users/profile/{username}'.format(username=self.username)

        data = await self.get(request_url, output='json')
        self._update_data(data)

        if return_:
            return data

    def _get_basetype_from_author_data(self, key, type_='int'):
        import builtins

        n = self.author_data.get(key, None)
        return getattr(builtins, type_)(n) if n else None

    def _get_str_from_author_data(self, key):
        n = self.author_data.get(key, None)
        return str(n) if n else None

    @property
    def username(self):
        return self._get_basetype_from_author_data('username', 'str')

    @property
    def avatar(self):
        return self._get_basetype_from_author_data('avatar', 'str')

    @property
    def donate_url(self):
        return self._get_basetype_from_author_data('donateUrl', 'str')

    @property
    def socials(self):
        return self._get_basetype_from_author_data('socials', 'list')

    @property
    def author_id(self):
        return self._get_basetype_from_author_data('_id', 'str')

    @property
    def name(self):
        return self._get_basetype_from_author_data('name', 'str')

    @property
    def description(self):
        return self._get_basetype_from_author_data('description', 'str')

    @property
    def description_short(self):
        return self._get_basetype_from_author_data('descriptionShort', 'str')

    @property
    def created_at(self):
        from datetime import datetime

        date = self.author_data.get('createdAt', None)

        if date:
            date = datetime.fromisoformat(date[:-1])

        return date

    @property
    def following_num(self):
        return self._get_basetype_from_author_data('followingNum', 'int')

    @property
    def followers_num(self):
        return self._get_basetype_from_author_data('followersNum', 'int')

    @property
    def read_num(self):
        return self._get_basetype_from_author_data('readNum', 'int')

    @property
    async def articles(self):
        from drukarnia_api.article import Article

        articles = self.author_data.get('articles', [])
        if not articles:
            return []

        tasks = [Article.from_records(self.session, **article) for article in articles]

        return await asyncio.gather(*tasks)

    @property
    async def author_tags(self):
        from drukarnia_api.tags import Tag

        tags = self.author_data.get('authorTags', [])
        if not tags:
            return []

        tasks = [Tag.from_records(self.session, **tag) for tag in tags]

        return await asyncio.gather(*tasks)

    def _update_data(self, new_data: dict):
        self.author_data.update(new_data)

    @staticmethod
    async def from_records(session: ClientSession, new_data: dict) -> 'Author':
        """
        Create an Author instance from records.
        """

        new_author = Author(session=session)
        new_author._update_data(new_data)

        return new_author

    def __hash__(self):
        return hash(self.author_id or self.username)
