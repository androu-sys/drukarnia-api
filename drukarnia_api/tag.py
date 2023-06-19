from aiohttp import ClientSession

from drukarnia_api.drukarnia_base import DrukarniaElement
from drukarnia_api.shortcuts import data2articles

from typing import TYPE_CHECKING, Tuple, Dict

if TYPE_CHECKING:   # always False, used for type hints
    from drukarnia_api.article import Article


class Tag(DrukarniaElement):
    def __init__(self, slug_name: str = None, tag_id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update the data with slug_name and tag_id
        self._update_data({'slug': slug_name, '_id': tag_id})

    @DrukarniaElement._control_attr('slug')
    async def get_articles(self, create_articles: bool = True, isolated: bool = False,
                           offset: int = 0, results_per_page: int = 20, n_collect: int = None,
                           *args, **kwargs) -> Tuple['Article'] or Tuple[Dict]:
        """
        Get the followers of the author.
        """

        new_headers = self.session.headers
        if isolated and new_headers.get('Cookie', None):
            del new_headers['Cookie']

        # Make a request to get the followers of the author
        articles = await self.multi_page_request(f'https://drukarnia.com.ua/themes/{self.slug}',
                                                 offset, results_per_page, n_collect, list_key='articles',
                                                 headers=new_headers, *args, **kwargs)
        if create_articles:
            articles = await data2articles(articles, self.session)

        return articles

    @DrukarniaElement._control_attr('slug')
    async def collect_data(self, return_: bool = False):
        result = await self.get(f'https://drukarnia.com.ua/themes/{self.slug}?page=1', output='json')

        if result.get('articles', None):
            del result['articles']

        self._update_data(result)

        if return_:
            return result

    @property
    def slug(self):
        """
        Get the slug property of the Tag.
        """
        return self._access_data('slug', str)

    @property
    def created_at(self):
        """
        Get the created_at property of the Tag.
        """
        return self._get_datetime_from_author_data('createdAt')

    @property
    def default(self):
        """
        Get the default property of the Tag.
        """
        return self._get_basetype_from_data('default', bool)

    @property
    def mentions_num(self):
        """
        Get the mentions_num property of the Tag.
        """
        return self._get_basetype_from_data('mentionsNum', int)

    @property
    def name(self):
        """
        Get the name property of the Tag.
        """
        return self._access_data('name', None)

    @property
    def _id(self):
        """
        Get the _id property of the Tag.
        """
        return self._access_data('_id', None)

    @property
    def relationships(self):
        return self._access_data('relationships', None)

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
