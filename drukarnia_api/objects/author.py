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
        """
        Initialize an Author object.

        Parameters:
            username (str, optional): The username of the author. Defaults to None.
            author_id (str, optional): The ID of the author. Defaults to None.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self._update_data({'username': username, '_id': author_id})

    async def login(self, email: str, password: str) -> None:
        """
        Log in the author with the provided email and password.

        Parameters:
            email (str): The email of the author.
            password (str): The password of the author.

        Returns:
            None
        """

        await self.cookies.login(email, password, self)
        self._update_data(self.cookies.owner['user'])

    @DrukarniaElement.requires_attributes(['author_id'])
    async def get_followers(self, create_authors: bool = True, offset: int = 0, results_per_page: int = 20,
                            n_collect: int = None, *args, **kwargs) -> Tuple['Author'] or Tuple[Dict]:
        """
        Get the followers of the author.

        Parameters:
            create_authors (bool, optional): Whether to create Author objects for followers. Defaults to True.
            offset (int, optional): Offset for pagination. Defaults to 0.
            results_per_page (int, optional): Number of results per page for pagination. Defaults to 20.
            n_collect (int, optional): Total number of results to collect. Defaults to None.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Tuple['Author'] or Tuple[Dict]: A tuple of Author objects or dictionaries representing the followers.
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

        Parameters:
            create_authors (bool, optional): Whether to create Author objects for followings. Defaults to True.
            offset (int, optional): Offset for pagination. Defaults to 0.
            results_per_page (int, optional): Number of results per page for pagination. Defaults to 20.
            n_collect (int, optional): Total number of results to collect. Defaults to None.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Tuple['Author'] or Tuple[Dict]: A tuple of Author objects or dictionaries representing the followings.
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

        Parameters:
            offset (int, optional): Offset for pagination. Defaults to 0.
            results_per_page (int, optional): Number of results per page for pagination. Defaults to 20.
            n_collect (int, optional): Total number of results to collect. Defaults to None.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            List[Dict]: A list of dictionaries representing the notifications.
        """
        return await self.multi_page_request('/api/notifications',
                                             offset, results_per_page, n_collect,
                                             *args, **kwargs)

    async def get_reads_history(self, create_articles: bool = True, offset: int = 0,
                                results_per_page: int = 20, n_collect: int = None,
                                *args, **kwargs) -> List[Dict] or List['Article']:
        """
        Get the reading history of the author.

        Parameters:
            create_articles (bool, optional): Whether to create Article objects for read history. Defaults to True.
            offset (int, optional): Offset for pagination. Defaults to 0.
            results_per_page (int, optional): Number of results per page for pagination. Defaults to 20.
            n_collect (int, optional): Total number of results to collect. Defaults to None.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            List[Dict] or List['Article']: A list of dictionaries or Article objects representing the reading history.
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

        Parameters:
            preview (bool, optional): Whether to get sections with preview. Defaults to True.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            List[dict]: A list of dictionaries representing the sections.
        """
        return await self.request('get', f'/api/articles/bookmarks/lists?preview={str(preview).lower()}',
                                  output='json', **kwargs)

    async def create_section(self, name: str, **kwargs) -> List[Dict]:
        """
        Create a new section for the author's articles.

        Parameters:
            name (str): The name of the new section.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            List[Dict]: A list of dictionaries representing the new section.
        """
        section_id = await self.request('get',
                                        '/api/articles/bookmarks/lists',
                                        data={"name": name},
                                        output='read', **kwargs)

        return section_id.decode('utf-8')

    async def delete_section(self, section_id: str, **kwargs) -> None:
        """
        Delete a section for the author's articles.

        Parameters:
            section_id (str): The ID of the section to be deleted.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        await self.request('delete', f'/api/articles/bookmarks/lists/{section_id}', **kwargs)

    @DrukarniaElement.requires_attributes(['author_id'])
    async def subscribe(self, unsubscribe: bool = False) -> None:
        """
        Subscribe or unsubscribe to/from an author.

        Parameters:
            unsubscribe (bool, optional): Whether to unsubscribe. Defaults to False.

        Returns:
            None
        """

        if unsubscribe:
            await self.request('delete', f'/api/relationships/subscribe/{await self.author_id}')
            return None

        await self.request('post', f'/api/relationships/subscribe/{await self.author_id}')

    @DrukarniaElement.requires_attributes(['author_id'])
    async def block(self, unblock: bool = False) -> None:
        """
        Block or unblock an author.

        Parameters:
            unblock (bool, optional): Whether to unblock. Defaults to False.

        Returns:
            None
        """

        if unblock:
            await self.request('patch', f'/api/relationships/block/{await self.author_id}')
            return None

        await self.request('put', f'/api/relationships/block/{await self.author_id}')

    async def get_blocked(self, create_authors: bool = False) -> List[Dict] or Tuple['Author']:
        """
        Get the authors blocked by the current author.

        Parameters:
            create_authors (bool, optional): Whether to create Author objects for blocked authors. Defaults to False.

        Returns:
            List[Dict] or Tuple['Author']: A list of dictionaries or Author objects representing the blocked authors.
        """

        authors = await self.request('get', '/api/relationships/blocked', output='json')

        if create_authors:
            authors = await data2authors(authors, self.session)

        return authors

    async def change_password(self, old_password: str, new_password: str, **kwargs) -> None:
        """
        Change the author's password.

        Parameters:
            old_password (str): The current password of the author.
            new_password (str): The new password for the author.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        await self.request('patch', f'/api/users/login/password',
                           data={"oldPassword": old_password, "newPassword": new_password},
                           output='read', **kwargs)

    async def change_user_info(self, name: str = None, description: str = None, username: str = None,
                               description_short: str = None, socials: dict = None, donate_url: str = None) -> str:
        """
        Change the author's user information.

        Parameters:
            name (str, optional): The new name of the author. Defaults to None.
            description (str, optional): The new description of the author. Defaults to None.
            username (str, optional): The new username of the author. Defaults to None.
            description_short (str, optional): The new short description of the author. Defaults to None.
            socials (dict, optional): The new socials information of the author. Defaults to None.
            donate_url (str, optional): The new donate URL of the author. Defaults to None.

        Returns:
            str: The response received from the server.
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

        Parameters:
            current_password (str): The current password of the author.
            new_email (str): The new email for the author.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        await self.request('patch', f'/api/users/login/email',
                           data={"currentPassword": current_password, "newEmail": new_email},
                           **kwargs)

    @DrukarniaElement.requires_attributes(['username'], solution='provide username while initializing Author.')
    async def collect_data(self, return_: bool = False) -> Dict or None:
        """
        Collect the author's data and update the object's attributes.

        Parameters:
            return_ (bool, optional): Whether to return the collected data. Defaults to False.

        Returns:
            Dict or None: A dictionary representing the author's data if return_ is True, otherwise None.
        """

        data = await self.request('get', '/api/users/profile/{username}'.format(username=await self.username),
                                  output='json')

        self._update_data(data)

        if return_:
            return data

    @property
    @DrukarniaElement.type_decorator(str)
    async def username(self) -> str:
        """
        Get the username of the author.

        Returns:
            str: The username of the author.
        """
        return self._access_data('username')

    @property
    @DrukarniaElement.type_decorator(str)
    async def avatar(self) -> str:
        """
        Get the avatar of the author.

        Returns:
            str: The avatar URL of the author.
        """
        return self._access_data('avatar')

    @property
    @DrukarniaElement.type_decorator(str)
    async def donate_url(self) -> str:
        """
        Get the donate URL of the author.

        Returns:
            str: The donate URL of the author.
        """
        return self._access_data('donateUrl')

    @property
    @DrukarniaElement.type_decorator(str)
    async def socials(self) -> Dict:
        """
        Get the socials information of the author.

        Returns:
            Dict: A dictionary representing the socials information of the author.
        """
        return self._access_data('socials')

    @property
    @DrukarniaElement.type_decorator(str)
    async def author_id(self) -> str:
        """
        Get the ID of the author.

        Returns:
            str: The ID of the author.
        """
        return self._access_data('_id')

    @property
    @DrukarniaElement.type_decorator(str)
    async def name(self) -> str:
        """
        Get the name of the author.

        Returns:
            str: The name of the author.
        """
        return self._access_data('name')

    @property
    @DrukarniaElement.type_decorator(str)
    async def description(self) -> str:
        """
        Get the description of the author.

        Returns:
            str: The description of the author.
        """
        return self._access_data('description')

    @property
    @DrukarniaElement.type_decorator(str)
    async def description_short(self) -> str:
        """
        Get the short description of the author.

        Returns:
            str: The short description of the author.
        """
        return self._access_data('descriptionShort')

    @property
    @DrukarniaElement.type_decorator(datetime)
    async def created_at(self) -> datetime:
        """
        Get the creation date of the author.

        Returns:
            datetime: The creation date of the author.
        """
        return self._access_data('createdAt')

    @property
    @DrukarniaElement.type_decorator(int)
    async def following_num(self) -> int:
        """
        Get the number of authors the current author is following.

        Returns:
            int: The number of authors the current author is following.
        """
        return self._access_data('followingNum')

    @property
    @DrukarniaElement.type_decorator(int)
    async def followers_num(self) -> int:
        """
        Get the number of followers of the author.

        Returns:
            int: The number of followers of the author.
        """
        return self._access_data('followersNum')

    @property
    @DrukarniaElement.type_decorator(int)
    async def read_num(self) -> int:
        """
        Get the number of reads by the author.

        Returns:
            int: The number of reads by the author.
        """
        return self._access_data('readNum')

    @property
    async def articles(self) -> Tuple['Article']:
        """
        Get the articles written by the author.

        Returns:
            Tuple['Article']: A tuple of Article objects representing the articles written by the author.
        """
        return await data2articles(self._access_data('articles', []), self.session)

    @property
    async def author_tags(self) -> Tuple['Tag']:
        """
        Get the tags associated with the author.

        Returns:
            Tuple['Tag']: A tuple of Tag objects representing the tags associated with the author.
        """
        return await data2tags(self._access_data('authorTags', []), self.session)

    @property
    @DrukarniaElement.type_decorator(dict)
    async def relationships(self) -> Dict:
        """
        Get the relationships of the author.

        Returns:
            Dict: A dictionary representing the relationships of the author.
        """
        return self._access_data('relationships')

    @property
    @DrukarniaElement.type_decorator(bool)
    async def is_subscribed(self) -> bool:
        """
        Get the subscription state.

        Returns:
            Bool: True if you follow this author, otherwise False
        """
        return self._access_data('relationships', {}).get('isSubscribed', None)

    @property
    @DrukarniaElement.type_decorator(bool)
    async def is_blocked(self) -> bool:
        """
        Get the blocked state.

        Returns:
            Bool: True if you blocked this author, otherwise False
        """
        return self._access_data('relationships', {}).get('isBlocked', None)

    @staticmethod
    async def from_records(session: ClientSession, new_data: Dict) -> 'Author':
        """
        Create an Author instance from records.

        Parameters:
            session (ClientSession): The aiohttp client session.
            new_data (dict): The data to create the Author instance.

        Returns:
            Author: An Author instance.
        """

        new_author = Author(session=session)
        new_author._update_data(new_data)

        return new_author

    def __hash__(self) -> int:
        """
        Calculate the hash value for the Author object.

        Returns:
            int: The hash value.
        """
        return hash(self.author_id or self.username)
