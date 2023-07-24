from datetime import datetime
from warnings import warn
from aiohttp import ClientSession

from drukarnia_api.objects.base_object import DrukarniaElement
from drukarnia_api.shortcuts import data2authors, data2articles, data2tags, data2comments

from typing import TYPE_CHECKING, Tuple, Dict

if TYPE_CHECKING:  # always False, used for type hints
    from drukarnia_api.objects.author import Author
    from drukarnia_api.objects.tag import Tag
    from drukarnia_api.objects.comment import Comment


class Article(DrukarniaElement):
    def __init__(self, slug: str = None, article_id: str = None, *args, **kwargs):
        """
        Initializes an Article object with the given slug and article ID.

        Parameters:
        - slug (str): The slug of the article.
        - article_id (str): The ID of the article.
        """

        super().__init__(*args, **kwargs)

        self._update_data({'slug': slug, '_id': article_id})

    @DrukarniaElement.requires_attributes(['article_id'])
    async def post_comment(self, comment_text: str) -> str:
        """
        Posts a comment on the article and returns the ID of the posted comment.

        Parameters:
        - comment_text (str): The text of the comment to be posted.

        Returns:
        - str: The ID of the posted comment.
        """

        posted_comment_id = await self.request(
            'post',
            '/api/articles/{_id}/comments'.format(_id=await self.article_id),
            data={'comment': comment_text}, output='read')

        return str(posted_comment_id)

    @DrukarniaElement.requires_attributes(['article_id'])
    async def like_article(self, n_likes: int) -> None:
        """
        Likes the article with the specified number of likes.

        Parameters:
        - n_likes (int): The number of likes to be added to the article.

        Raises:
        - ValueError: If the number of likes is not between 0 and 10 (inclusive).
        """

        assert 0 < n_likes <= 10, 'Number of likes must be greater or equal to zero and lower or equal to ten'

        await self.request(
            'post',
            f'/api/articles/{await self.article_id}/like',
            data={'likes': int(n_likes)})

    @DrukarniaElement.requires_attributes(['article_id'])
    async def bookmark(self, section_id: str, unbookmark: bool = False) -> None:
        """
        Adds or removes the article from bookmarks based on the 'unbookmark' parameter.

        Parameters:
        - section_id (str): The ID of the section to bookmark the article.
        - unbookmark (bool): If True, removes the article from bookmarks. If False, adds it to bookmarks.

        Raises:
        - ValueError: If section_id is not provided for bookmarking.
        """

        if unbookmark:
            await self.request('delete', f'/api/articles/{await self.article_id}/bookmarks')

        elif not section_id:
            raise ValueError('section_id must be passed for bookmarking')

        else:
            await self.request('post', '/api/articles/bookmarks',
                               data={"article": await self.article_id, "list": section_id})

    @DrukarniaElement.requires_attributes(['slug'])
    async def collect_data(self, return_: bool = False) -> Dict or None:
        """
        Collects the article's data and updates the object's attributes.

        Parameters:
        - return_ (bool): If True, returns the collected data.

        Returns:
        - Dict or None: The collected data if 'return_' is True, otherwise None.
        """

        data = await self.request('get', f'/api/articles/{await self.slug}', output='json')

        self._update_data(data)

        if return_:
            return data

    @property
    async def owner(self) -> 'Author' or None:
        """
        Retrieves the owner of the article.

        Returns:
        - 'Author' or None: The owner of the article if available, otherwise None.
        """

        owner = self._access_data('owner', None)
        if owner is None:
            return None

        return await data2authors([owner], self.session)

    @property
    async def comments(self) -> Tuple['Comment']:
        """
        Retrieves the comments of the article.

        Returns:
        - Tuple['Comment']: A tuple containing the comments of the article.
        """

        return await data2comments(self._access_data('comments', []), self.session)

    @property
    async def recommended_articles(self) -> Tuple['Article']:
        """
        Retrieves the recommended articles related to the article.

        Returns:
        - Tuple['Article']: A tuple containing the recommended articles.
        """

        return await data2articles(self._access_data('recommendedArticles', []), self.session)

    @property
    async def author_articles(self) -> Tuple['Article']:
        """
        Retrieves the articles written by the author of the article.

        Returns:
        - Tuple['Article']: A tuple containing the articles written by the author.
        """

        return await data2articles(self._access_data('authorArticles', []), self.session)

    @property
    @DrukarniaElement.type_decorator(dict)
    async def relationships(self) -> Dict:
        """
        Retrieves the relationships of the article.

        Returns:
        - Dict: The relationships of the article.
        """

        return self._access_data('relationships')

    @property
    @DrukarniaElement.type_decorator(bool)
    async def is_bookmarked(self) -> bool:
        """
        Checks if the article is bookmarked.

        Returns:
        - bool: True if the article is bookmarked, False otherwise.
        """

        return self._access_data('isBookmarked')

    @property
    @DrukarniaElement.type_decorator(int)
    async def my_likes(self) -> int:
        """
        Checks if the article is liked.

        Returns:
        - bool: True if the article is liked, False otherwise.
        """

        return self._access_data('isLiked')

    @property
    @DrukarniaElement.type_decorator(bool)
    async def sensitive(self) -> bool:
        """
        Checks if the article is sensitive.

        Returns:
        - bool: True if the article is sensitive, False otherwise.
        """

        return self._access_data('sensitive')

    @property
    @DrukarniaElement.type_decorator(dict)
    async def content(self) -> Dict:
        """
        Retrieves the content of the article.

        Returns:
        - Dict: The content of the article.
        """

        return self._access_data('content')

    @property
    @DrukarniaElement.type_decorator(str)
    async def thumb_picture(self) -> str:
        """
        Retrieves the thumbnail picture of the article.

        Returns:
        - str: The URL of the thumbnail picture.
        """

        return self._access_data('thumbPicture')

    @property
    @DrukarniaElement.type_decorator(str)
    async def picture(self) -> str:
        """
        Retrieves the picture of the article.

        Returns:
        - str: The URL of the picture.
        """

        return self._access_data('picture')

    @property
    @DrukarniaElement.type_decorator(str)
    async def ads(self) -> str:
        """
        Retrieves the ads of the article.

        Returns:
        - str: The ads of the article.
        """

        return self._access_data('ads')

    @property
    @DrukarniaElement.type_decorator(str)
    async def index(self) -> str:
        """
        Retrieves the index of the article.

        Returns:
        - str: The index of the article.
        """

        return self._access_data('index')

    @property
    @DrukarniaElement.type_decorator(datetime)
    async def created_at(self) -> datetime:
        """
        Retrieves the creation date of the article.

        Returns:
        - datetime: The creation date of the article.
        """

        return self._access_data('createdAt')

    @property
    @DrukarniaElement.type_decorator(float)
    async def read_time(self) -> float:
        """
        Retrieves the read time of the article.

        Returns:
        - float: The read time of the article.
        """

        return self._access_data('readTime')

    @property
    @DrukarniaElement.type_decorator(int)
    async def number_of_likes(self) -> int:
        """
        Retrieves the number of likes of the article.

        Returns:
        - int: The number of likes of the article.
        """

        return self._access_data('likeNum')

    @property
    @DrukarniaElement.type_decorator(int)
    async def number_of_comments(self) -> int:
        """
        Retrieves the number of comments of the article.

        Returns:
        - int: The number of comments of the article.
        """

        return self._access_data('commentNum')

    @property
    async def article_tags(self) -> Tuple['Tag']:
        """
        Retrieves the tags of the article.

        Returns:
        - Tuple['Tag']: A tuple containing the tags of the article.
        """

        tags = self._access_data('tags', [])

        if any(map(lambda el: isinstance(el, str), tags)):
            warn("Tag's data is incomplete, use collect_data method before in order to obtain whole data.")
            tags = map(lambda el: {'_id': el}, tags)

        return await data2tags(tags, self.session)

    @property
    async def main_article_tag(self) -> 'Tag' or None:
        """
        Retrieves the main tag of the article.

        Returns:
        - 'Tag' or None: The main tag of the article if available, otherwise None.
        """

        main_id = self._access_data('mainTagId', str)
        main_name = self._access_data('mainTag', str)
        main_slug = self._access_data('mainTagSlug', str)

        if not (main_id and main_name and main_slug):
            return None

        main_tag, = await data2tags([{'_id': main_id, 'name': main_name, 'slug': main_slug}], self.session)

        return main_tag

    @property
    @DrukarniaElement.type_decorator(str)
    async def description(self) -> str:
        """
        Retrieves the description of the article.

        Returns:
        - str: The description of the article.
        """

        return self._access_data('description')

    @property
    @DrukarniaElement.type_decorator(str)
    async def seo_title(self) -> str:
        """
        Retrieves the SEO title of the article.

        Returns:
        - str: The SEO title of the article.
        """
        return self._access_data('seoTitle')

    @property
    @DrukarniaElement.type_decorator(str)
    async def title(self) -> str:
        """
        Retrieves the title of the article.

        Returns:
        - str: The title of the article.
        """
        return self._access_data('title')

    @property
    @DrukarniaElement.type_decorator(str)
    async def article_id(self) -> str:
        """
        Retrieves the ID of the article.

        Returns:
        - str: The ID of the article.
        """
        return self._access_data('_id')

    @property
    @DrukarniaElement.type_decorator(str)
    async def slug(self) -> str:
        """
        Retrieves the slug of the article.

        Returns:
        - str: The slug of the article.
        """
        return self._access_data('slug')

    @staticmethod
    async def from_records(session: ClientSession, new_data: dict) -> 'Article':
        """
        Creates an Article instance from records.

        Parameters:
        - session (ClientSession): The client session.
        - new_data (dict): The new data to create the Article instance.

        Returns:
        - 'Article': The created Article instance.
        """

        new_article = Article(session=session)
        new_article._update_data(new_data)

        return new_article

    def __hash__(self) -> int:
        """
        Returns the hash value of the Article object.

        Returns:
        - int: The hash value of the Article object.
        """
        return hash(self.article_id or self.slug)
