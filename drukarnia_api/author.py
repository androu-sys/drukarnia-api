import re
from typing import Iterable, Any, Dict, List
from warnings import warn

from aiohttp import ClientSession
from drukarnia_api.drukarnia_base.element import DrukarniaElement
from drukarnia_api.shortcuts.class_generator import data2authors, data2articles     # data2tags


class Author(DrukarniaElement):
    def __init__(self, username: str = None, author_id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._update_data({'username': username, '_id': author_id})

    async def login(self, email: str, password: str) -> None:
        """
        Log in the author with the provided email and password.
        """

        headers, info = await self.post('/api/users/login',
                                        data={'password': password, 'email': email},
                                        output=['headers', 'json'])

        if self.author_id and (self.author_id != info['user']['_id']):
            raise ValueError('You are trying to log into an unrelated author.')

        elif self.username and (self.username != info['user']['username']):
            raise ValueError('You are trying to log into an unrelated author.')

        elif not (self.author_id or self.username):
            warn("We weren't able to identify any relationship between the current Author data and the Drukarnia "
                 "User you are trying to log into. It may cause unexpected and fatal errors. Please consider "
                 "initializing the Author class with a username or _id. Alternatively, run the collect_data "
                 "method first!")

        headers = str(headers)

        token = re.search(r'refreshToken=(.*?);', headers).group(1)
        device_id = re.search(r'deviceId=(.*?);', headers).group(1)

        self.session.headers.update({'Cookie': f'deviceId={device_id}; token={token};'})

    async def get_followers(self, create_authors: bool = True, offset: int = 0, results_per_page: int = 20,
                            n_collect: int = None, *args, **kwargs) -> Iterable['Author']:
        """
        Get the followers of the author.
        """
        self._control_attr('author_id')

        request_url = '/api/relationships/{user_id}/followers'.format(user_id=self.author_id)

        # Make a request to get the followers of the author
        followers = await self.multi_page_request(request_url, offset, results_per_page, n_collect, *args, **kwargs)

        if create_authors:
            followers = await data2authors(followers, self.session)

        return followers

    async def get_followings(self, create_authors: bool = True, offset: int = 0, results_per_page: int = 20,
                             n_collect: int = None, *args, **kwargs) -> Iterable['Author']:
        """
        Get the followings of the author.
        """

        self._control_attr('author_id')

        request_url = '/api/relationships/{user_id}/following'.format(user_id=self.author_id)

        # Make a request to get the followings of the author
        followings = await self.multi_page_request(request_url, offset, results_per_page, n_collect, *args, **kwargs)

        if create_authors:
            followings = await data2authors(followings, self.session)

        return followings

    @DrukarniaElement._is_authenticated
    async def get_notifications(self, offset: int = 0, results_per_page: int = 20,
                                n_collect: int = None, *args, **kwargs) -> Iterable[list or dict]:
        """
        Get the notifications of the author.
        """

        return await self.multi_page_request('/api/notifications',
                                             offset, results_per_page, n_collect,
                                             *args, **kwargs)

    @DrukarniaElement._is_authenticated
    async def get_reads_history(self, offset: int = 0, results_per_page: int = 20,
                                n_collect: int = None, *args, **kwargs) -> Iterable[list or dict]:
        """
        Get the reading history of the author.
        """
        return await self.multi_page_request('/api/stats/reads/history',
                                             offset, results_per_page, n_collect,
                                             *args, **kwargs)

    @DrukarniaElement._is_authenticated
    async def get_sections(self, preview: bool = True, *args, **kwargs) -> Iterable[list or dict]:
        """
        Get the sections of the author's articles.
        """

        return await self.get(f'/api/articles/bookmarks/lists?preview={str(preview).lower()}',
                              output='json', *args, **kwargs)

    @DrukarniaElement._is_authenticated
    async def create_section(self, name: str, **kwargs) -> Any:
        """
        Create a new section for the author's articles.
        """
        return await self.post('/api/articles/bookmarks/lists', data={"name": name}, output='read', **kwargs)

    @DrukarniaElement._is_authenticated
    async def delete_section(self, section_id: str, **kwargs) -> Any:
        """
        Delete a section for the author's articles.
        """
        return await self.delete(f'/api/articles/bookmarks/lists/{section_id}', **kwargs)

    @DrukarniaElement._is_authenticated
    async def subscribe(self, author_id: str, unsubscribe: bool = False) -> None:
        if unsubscribe:
            await self.delete(f'/api/relationships/subscribe/{author_id}')
            return None

        await self.post(f'/api/relationships/subscribe/{author_id}')

    @DrukarniaElement._is_authenticated
    async def block(self, author_id: str, unblock: bool = False) -> None:
        if unblock:
            await self.patch(f'/api/relationships/block/{author_id}')
            return None

        await self.put(f'/api/relationships/block/{author_id}')

    @DrukarniaElement._is_authenticated
    async def get_blocked(self) -> Iterable[list or dict]:
        """
        Get the authors blocked by the current author.
        """
        return await self.get('/api/relationships/blocked')

    @DrukarniaElement._is_authenticated
    async def change_password(self, old_password: str, new_password: str, **kwargs) -> str:
        """
        Change the author's password.
        """

        return await self.patch(f'/api/users/login/password',
                                data={"oldPassword": old_password, "newPassword": new_password},
                                output='read', **kwargs)

    @DrukarniaElement._is_authenticated
    async def change_user_info(self, name: str = None, description: str = None, username: str = None,
                               description_short: str = None, socials: dict = None, donate_url: str = None) -> str:
        """
        Change the author's user information.
        """

        info2patch = {"name": name, "description": description, "username": username,
                      "descriptionShort": description_short,
                      "socials": socials, "donateUrl": donate_url}

        info2patch = {key: value for key, value in info2patch.items() if value is not None}

        response = await self.patch('/api/users', data=info2patch, output='read')
        return response

    @DrukarniaElement._is_authenticated
    async def change_email(self, current_password: str, new_email: str, **kwargs) -> str:
        """
        Change the author's email.
        """

        return await self.patch(f'/api/users/login/email',
                                data={"currentPassword": current_password, "newEmail": new_email},
                                output='read', **kwargs)

    async def collect_data(self, return_: bool = False) -> dict or None:
        """
        Collect the author's data and update the object's attributes.
        """

        self._control_attr('username')

        data = await self.get('/api/users/profile/{username}'.format(username=self.username),
                              output='json')

        self._update_data(data)

        if return_:
            return data

    @property
    def username(self):
        return self._get_basetype_from_author_data('username', str)

    @property
    def avatar(self):
        return self._get_basetype_from_author_data('avatar', str)

    @property
    def donate_url(self):
        return self._get_basetype_from_author_data('donateUrl', str)

    @property
    def socials(self) -> Dict:
        return self._get_basetype_from_author_data('socials', dict)

    @property
    def author_id(self):
        return self._get_basetype_from_author_data('_id', str)

    @property
    def name(self):
        return self._get_basetype_from_author_data('name', str)

    @property
    def description(self):
        return self._get_basetype_from_author_data('description', str)

    @property
    def description_short(self):
        return self._get_basetype_from_author_data('descriptionShort', str)

    @property
    def created_at(self):
        return self._get_datetime_from_author_data('createdAt')

    @property
    def following_num(self):
        return self._get_basetype_from_author_data('followingNum', int)

    @property
    def followers_num(self):
        return self._get_basetype_from_author_data('followersNum', int)

    @property
    def read_num(self):
        return self._get_basetype_from_author_data('readNum', int)

    @property
    async def articles(self) -> List:
        return await data2articles(self._access_data('articles', []), self.session)

    @property
    async def author_tags(self) -> List:
        return self._access_data('authorTags', [])  # await data2tags(self._access_data('authorTags', []), self.session)

    @property
    def relationships(self):
        return self._get_basetype_from_author_data('relationships', dict)

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
