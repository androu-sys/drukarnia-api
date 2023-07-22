from datetime import datetime

from aiohttp import ClientSession

from drukarnia_api.objects.base_object import DrukarniaElement
from drukarnia_api.shortcuts import data2articles, data2tags, data2authors

from typing import TYPE_CHECKING, Tuple, Dict

if TYPE_CHECKING:   # always False, used for type hints
    from drukarnia_api.objects.article import Article
    from drukarnia_api.objects.author import Author


class Tag(DrukarniaElement):
    def __init__(self, slug_name: str = None, tag_id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update the data with slug_name and tag_id
        self._update_data({'slug': slug_name, '_id': tag_id})

    @DrukarniaElement.requires_attributes(['slug'])
    async def get_articles(self, create_articles: bool = True,
                           offset: int = 0, results_per_page: int = 20, n_collect: int = None,
                           **kwargs) -> Tuple['Article'] or Tuple[Dict]:
        """
        Get the followers of the author.
        """

        # Make a request to get the followers of the author
        articles = await self.multi_page_request(f'/api/articles/tags/{await self.slug}',
                                                 offset, results_per_page, n_collect, list_key='articles',
                                                 **kwargs)
        if create_articles:
            articles = await data2articles(articles, self.session)

        return articles

    @DrukarniaElement.requires_attributes(['tag_id'])
    async def related_tags(self, create_tags: bool = True) -> Tuple['Tag'] or Tuple[Dict]:
        """
        Get the followers of the author.
        """

        # Make a request to get the followers of the author
        tags = await self.request('get', f'/api/articles/tags/{await self.tag_id}/related?page=1', output='json')
        if create_tags:
            tags = await data2tags(tags, self.session)

        return tags

    @DrukarniaElement.requires_attributes(['tag_id'])
    async def subscribe_tag(self, unsubscribe: bool = False) -> None:
        """
        Subscribe or unsubscribe to/from a tag.
        """
        if unsubscribe:
            await self.request('delete', f'/api/preferences/tags/{await self.tag_id}')
            return None

        await self.request('put', f'/api/preferences/tags/{await self.tag_id}')

    @DrukarniaElement.requires_attributes(['tag_id'])
    async def block_tag(self, unblock: bool = False) -> None:
        """
        Block or unblock an author.
        """
        if unblock:
            await self.request('put', f'/api/preferences/tags/{await self.tag_id}/block', data={"isBlocked": False})
            return None

        await self.request('put', f'/api/preferences/tags/{await self.tag_id}/block', data={"isBlocked": True})

    @DrukarniaElement.requires_attributes(['tag_id'])
    async def related_authors(self, create_tags: bool = True,) -> Tuple['Author'] or Tuple[Dict]:
        """
        Get the followers of the author.
        """

        # Make a request to get the followers of the author
        authors = await self.request('get', f'/api/users/tags/{await self.tag_id}/related', output='json')
        if create_tags:
            authors = await data2authors(authors, self.session)

        return authors

    @DrukarniaElement.requires_attributes(['slug'])
    async def collect_data(self, return_: bool = False):
        result = await self.request('get', f'/api/articles/tags/{await self.slug}?page=1', output='json')

        if result.get('articles', None):
            del result['articles']

        self._update_data(result)

        if return_:
            return result

    @property
    @DrukarniaElement.type_decorator(str)
    async def slug(self):
        """
        Get the slug property of the Tag.
        """
        return self._access_data('slug')

    @property
    @DrukarniaElement.type_decorator(datetime)
    async def created_at(self):
        """
        Get the created_at property of the Tag.
        """
        return self._access_data('createdAt')

    @property
    @DrukarniaElement.type_decorator(bool)
    async def default(self):
        """
        Get the default property of the Tag.
        """
        return self._access_data('default')

    @property
    @DrukarniaElement.type_decorator(int)
    async def mentions_num(self):
        """
        Get the mentions_num property of the Tag.
        """
        return self._access_data('mentionsNum')

    @property
    @DrukarniaElement.type_decorator(str)
    async def name(self):
        """
        Get the name property of the Tag.
        """
        return self._access_data('name')

    @property
    @DrukarniaElement.type_decorator(str)
    async def tag_id(self):
        """
        Get the _id property of the Tag.
        """
        return self._access_data('_id')

    @property
    @DrukarniaElement.type_decorator(dict)
    async def relationships(self):
        return self._access_data('relationships')

    @staticmethod
    async def from_records(session: ClientSession, new_data: dict) -> 'Tag':
        """
        Create a new Tag instance from records.

        Args:
            session (ClientSession): A session object for making HTTP requests.
            new_data (dict): Data to update the new Tag instance with.

        Returns:
            Tag: A new instance of the Tag class.
        """
        new_tag = Tag(session=session)
        new_tag._update_data(new_data)

        return new_tag
