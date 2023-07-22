from datetime import datetime
from typing import Dict, Tuple, List
from aiohttp import ClientSession

from drukarnia_api.objects.base_object import DrukarniaElement
from drukarnia_api.shortcuts import data2authors, data2articles, data2tags

from typing import TYPE_CHECKING

if TYPE_CHECKING:   # always False, used for type hints
    from drukarnia_api.objects.article import Article
    from drukarnia_api.objects.tag import Tag


class Author(DrukarniaElement):
    def __init__(self, username: str = None, author_id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._update_data({'username': username, '_id': author_id})

    async def login(self, email: str, password: str) -> None:
        """
        Log in the author with the provided email and password.
        """

        self.cookieJar.login(email, password, self)

    @DrukarniaElement.requires_attributes(['author_id'])
    async def get_followers(self, create_authors: bool = True, offset: int = 0, results_per_page: int = 20,
                            n_collect: int = None, *args, **kwargs) -> Tuple['Author'] or Tuple[Dict]:
        """
        Get the followers of the author.
        """

        # Make a request to get the followers of the author
        followers = await self.multi_page_request(f'/api/relationships/{await self.author_id}/followers',
                                                  offset, results_per_page, n_collect, *args, **kwargs)

        if create_authors:
            followers = await data2authors(followers, self.session)

        return followers

    @DrukarniaElement.requires_attributes(['author_id'])
    async def get_followings(self, create_authors: bool = True, offset: int = 0, results_per_page: int = 20,
                             n_collect: int = None, *args, **kwargs) -> Tuple['Author'] or Tuple[Dict]:
        """
        Get the followings of the author.
        """

        # Make a request to get the followings of the author
        followings = await self.multi_page_request(f'/api/relationships/{await self.author_id}/following',
                                                   offset, results_per_page, n_collect, *args, **kwargs)

        if create_authors:
            followings = await data2authors(followings, self.session)

        return followings

    async def get_notifications(self, offset: int = 0, results_per_page: int = 20,
                                n_collect: int = None, *args, **kwargs) -> List[Dict]:
        """
        Get the notifications of the author.
        """
        return await self.multi_page_request('/api/notifications',
                                             offset, results_per_page, n_collect,
                                             *args, **kwargs)

    async def get_reads_history(self, create_articles: bool = True, offset: int = 0,
                                results_per_page: int = 20, n_collect: int = None,
                                *args, **kwargs) -> List[Dict] or List['Article']:
        """
        Get the reading history of the author.
        """
        articles = await self.multi_page_request('/api/stats/reads/history',
                                                 offset, results_per_page, n_collect,
                                                 *args, **kwargs)

        if create_articles:
            articles = await data2articles(articles, self.session)

        return articles

    async def get_sections(self, preview: bool = True, **kwargs) -> List[dict]:
        """
        Get the sections of the author's articles.
        """
        return await self.request('get', f'/api/articles/bookmarks/lists?preview={str(preview).lower()}',
                                  output='json', **kwargs)

    async def create_section(self, name: str, **kwargs) -> List[Dict]:
        """
        Create a new section for the author's articles.
        """
        section_id = await self.request('get',
                                        '/api/articles/bookmarks/lists',
                                        data={"name": name},
                                        output='read', **kwargs)

        return section_id.decode('utf-8')

    async def delete_section(self, section_id: str, **kwargs) -> None:
        """
        Delete a section for the author's articles.
        """
        await self.request('delete', f'/api/articles/bookmarks/lists/{section_id}', **kwargs)

    async def subscribe_author(self, author_id: str, unsubscribe: bool = False) -> None:
        """
        Subscribe or unsubscribe to/from an author.
        """

        if unsubscribe:
            await self.request('delete', f'/api/relationships/subscribe/{author_id}')
            return None

        await self.request('post', f'/api/relationships/subscribe/{author_id}')

    async def block_author(self, author_id: str, unblock: bool = False) -> None:
        """
        Block or unblock an author.
        """
        if unblock:
            await self.request('patch', f'/api/relationships/block/{author_id}')
            return None

        await self.request('put', f'/api/relationships/block/{author_id}')

    async def get_blocked(self, create_authors: bool = False) -> List[Dict] or Tuple['Author']:
        """
        Get the authors blocked by the current author.
        """

        authors = await self.request('get', '/api/relationships/blocked', output='json')

        if create_authors:
            authors = await data2authors(authors, self.session)

        return authors

    async def change_password(self, old_password: str, new_password: str, **kwargs) -> None:
        """
        Change the author's password.
        """
        await self.request('patch', f'/api/users/login/password',
                           data={"oldPassword": old_password, "newPassword": new_password},
                           output='read', **kwargs)

    async def change_user_info(self, name: str = None, description: str = None, username: str = None,
                               description_short: str = None, socials: dict = None, donate_url: str = None) -> str:
        """
        Change the author's user information.
        """
        info2patch = {"name": name, "description": description, "username": username,
                      "descriptionShort": description_short,
                      "socials": socials, "donateUrl": donate_url}

        info2patch = {key: value for key, value in info2patch.items() if value is not None}

        response = await self.request('patch', '/api/users', data=info2patch, output='read')
        return response.decode('utf-8')

    async def change_email(self, current_password: str, new_email: str, **kwargs) -> None:
        """
        Change the author's email.
        """
        await self.request('patch', f'/api/users/login/email',
                           data={"currentPassword": current_password, "newEmail": new_email},
                           **kwargs)

    @DrukarniaElement.requires_attributes(['username'])
    async def collect_data(self, return_: bool = False) -> Dict or None:
        """
        Collect the author's data and update the object's attributes.
        """

        data = await self.request('get', '/api/users/profile/{username}'.format(username=await self.username),
                                  output='json')

        self._update_data(data)

        if return_:
            return data

    @property
    @DrukarniaElement.type_decorator(str)
    async def username(self) -> str:
        return self._access_data('username')

    @property
    @DrukarniaElement.type_decorator(str)
    async def avatar(self) -> str:
        return self._access_data('avatar')

    @property
    @DrukarniaElement.type_decorator(str)
    async def donate_url(self) -> str:
        return self._access_data('donateUrl')

    @property
    @DrukarniaElement.type_decorator(str)
    async def socials(self) -> Dict:
        return self._access_data('socials')

    @property
    @DrukarniaElement.type_decorator(str)
    async def author_id(self) -> str:
        return self._access_data('_id')

    @property
    @DrukarniaElement.type_decorator(str)
    async def name(self) -> str:
        return self._access_data('name')

    @property
    @DrukarniaElement.type_decorator(str)
    async def description(self) -> str:
        return self._access_data('description')

    @property
    @DrukarniaElement.type_decorator(str)
    async def description_short(self) -> str:
        return self._access_data('descriptionShort')

    @property
    @DrukarniaElement.type_decorator(datetime)
    async def created_at(self) -> datetime:
        return self._access_data('createdAt')

    @property
    @DrukarniaElement.type_decorator(int)
    async def following_num(self) -> int:
        return self._access_data('followingNum')

    @property
    @DrukarniaElement.type_decorator(int)
    async def followers_num(self) -> int:
        return self._access_data('followersNum')

    @property
    @DrukarniaElement.type_decorator(int)
    async def read_num(self) -> int:
        return self._access_data('readNum')

    @property
    async def articles(self) -> Tuple['Article']:
        return await data2articles(self._access_data('articles', []), self.session)

    @property
    async def author_tags(self) -> Tuple['Tag']:
        return await data2tags(self._access_data('authorTags', []), self.session)

    @property
    @DrukarniaElement.type_decorator(dict)
    async def relationships(self) -> Dict:
        return self._access_data('relationships')

    @staticmethod
    async def from_records(session: ClientSession, new_data: dict) -> 'Author':
        """
        Create an Author instance from records.
        """
        new_author = Author(session=session)
        new_author._update_data(new_data)
        return new_author

    def __hash__(self) -> int:
        return hash(self.author_id or self.username)
