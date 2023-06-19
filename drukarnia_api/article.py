from datetime import datetime
from warnings import warn
from aiohttp import ClientSession

from drukarnia_api.drukarnia_base import DrukarniaElement
from drukarnia_api.shortcuts import data2authors, data2articles, data2tags

from typing import TYPE_CHECKING, Tuple, Dict, List

if TYPE_CHECKING:   # always False, used for type hints
    from drukarnia_api.author import Author
    from drukarnia_api.tag import Tag


class Article(DrukarniaElement):
    def __init__(self, slug: str = None, article_id: str = None, *args, **kwargs):
        """
        Initializes an Article object with the given slug and article ID.
        """
        super().__init__(*args, **kwargs)

        self._update_data({'slug': slug, '_id': article_id})

    @DrukarniaElement._control_attr('article_id')
    @DrukarniaElement._is_authenticated
    async def post_comment(self, comment_text: str) -> str:
        """
        Posts a comment on the article and returns the ID of the posted comment.
        """

        posted_comment_id = await self.post('/api/articles/{_id}/comments'.format(_id=self.article_id),
                                            {'comment': comment_text}, output='read')
        return str(posted_comment_id)

    @DrukarniaElement._control_attr('article_id')
    @DrukarniaElement._is_authenticated
    async def reply2comment(self, comment_text: str, comment_id: str, root_comment: str,
                            root_comment_owner: str, reply2user: str) -> str:
        """
        Posts a reply to a comment and returns the ID of the new comment.
        """

        new_comment_id = await self.post(
            f'/api/articles/{self.article_id}/comments/{comment_id}/replies',
            {
                "comment": comment_text, "replyToComment": comment_id, "rootComment": root_comment,
                "rootCommentOwner": root_comment_owner, "replyToUser": reply2user
            },
            output='read'
        )

        return str(new_comment_id)

    @DrukarniaElement._control_attr('article_id')
    @DrukarniaElement._is_authenticated
    async def delete_comment(self, comment_id: str) -> None:
        """
        Deletes a comment from the article.
        """

        await self.delete(f'/api/articles/{self.article_id}/comments/{comment_id}', [])

    @DrukarniaElement._control_attr('article_id')
    @DrukarniaElement._is_authenticated
    async def like_comment(self, comment_id: str, delete: bool = False) -> None:
        """
        Likes or unlikes a comment based on the 'delete' parameter.
        """

        if delete:
            await self.delete(f'/api/articles/{self.article_id}/comments/{comment_id}/likes', [])

        else:
            await self.post(f'/api/articles/{self.article_id}/comments/{comment_id}/likes', {}, [])

    @DrukarniaElement._control_attr('article_id')
    @DrukarniaElement._is_authenticated
    async def like_article(self, n_likes: int) -> None:
        """
        Likes the article with the specified number of likes.
        """

        if not (0 <= n_likes <= 10):
            raise ValueError('Number of likes must be greater or equal to zero and lower or equal to ten')

        await self.post(f'/api/articles/{self.article_id}/like', {'likes': n_likes}, 'read')

    @DrukarniaElement._control_attr('article_id')
    @DrukarniaElement._is_authenticated
    async def bookmark(self, section_id: str = '', unbookmark: bool = False) -> None:
        """
        Adds or removes the article from bookmarks based on the 'unbookmark' parameter.
        """

        if unbookmark:
            await self.delete(f'/api/articles/{self.article_id}/bookmarks', [])

        elif not section_id:
            raise ValueError('section_id must be passed to bookmark')

        else:
            await self.post('/api/articles/bookmarks', {"article": self.article_id, "list": section_id}, [])

    @DrukarniaElement._control_attr('slug')
    async def collect_data(self, return_: bool = False) -> Dict or None:
        """
        Collects the article's data and updates the object's attributes.
        If 'return_' is True, returns the collected data.
        """

        data = await self.get(f'/api/articles/{self.slug}', output='json')

        self._update_data(data)

        if return_:
            return data

    @property
    async def owner(self) -> 'Author' or None:
        """
        Retrieves the owner of the article.
        """
        owner = self._access_data('owner', None)
        if owner is None:
            return None

        return await data2authors([owner], self.session)

    @property
    def comments(self) -> List:
        """
        Retrieves the comments of the article.
        """
        return self._access_data('comments', [])

    @property
    async def recommended_articles(self) -> Tuple['Article']:
        """
        Retrieves the recommended articles related to the article.
        """
        return await data2articles(self._access_data('recommendedArticles', []), self.session)

    @property
    def relationships(self) -> Dict:
        """
        Retrieves the relationships of the article.
        """
        return self._get_basetype_from_data('relationships', dict)

    @property
    @DrukarniaElement._is_authenticated
    def is_bookmarked(self) -> bool:
        """
        Checks if the article is bookmarked.
        """
        return self._get_basetype_from_data('isBookmarked', bool)

    @property
    @DrukarniaElement._is_authenticated
    def is_liked(self) -> bool:
        """
        Checks if the article is liked.
        """
        return self._get_basetype_from_data('isLiked', bool)

    @property
    def sensitive(self) -> bool:
        """
        Checks if the article is sensitive.
        """
        return self._get_basetype_from_data('sensitive', bool)

    @property
    def content(self) -> Dict:
        """
        Retrieves the content of the article.
        """
        return self._get_basetype_from_data('content', dict)

    @property
    async def author_articles(self) -> Tuple['Article']:
        """
        Retrieves the articles written by the author of the article.
        """
        return await data2articles(self._access_data('authorArticles', []), self.session)

    @property
    def thumb_picture(self) -> str:
        """
        Retrieves the thumbnail picture of the article.
        """
        return self._get_basetype_from_data('thumbPicture', str)

    @property
    def picture(self) -> str:
        """
        Retrieves the picture of the article.
        """
        return self._get_basetype_from_data('picture', str)

    @property
    def ads(self) -> str:
        """
        Retrieves the ads of the article.
        """
        return self._get_basetype_from_data('ads', str)

    @property
    def index(self) -> str:
        """
        Retrieves the index of the article.
        """
        return self._get_basetype_from_data('index', str)

    @property
    def created_at(self) -> datetime:
        """
        Retrieves the creation date of the article.
        """
        return self._get_datetime_from_author_data('createdAt')

    @property
    def read_time(self) -> float:
        """
        Retrieves the read time of the article.
        """
        return self._get_basetype_from_data('readTime', float)

    @property
    def number_of_like(self) -> int:
        """
        Retrieves the number of likes of the article.
        """
        return self._get_basetype_from_data('description', int)

    @property
    def number_of_comment(self) -> int:
        """
        Retrieves the number of comments of the article.
        """
        return self._get_basetype_from_data('commentNum', int)

    @property
    async def article_tags(self) -> Tuple['Tag']:
        """
        Retrieves the tags of the article.
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
        """

        main_id = self._get_basetype_from_data('mainTagId', str)
        main_name = self._get_basetype_from_data('mainTag', str)
        main_slug = self._get_basetype_from_data('mainTagSlug', str)

        if not (main_id and main_name and main_slug):
            return None

        main_tag, = await data2tags([{'_id': main_id, 'name': main_name, 'slug': main_slug}], self.session)

        return main_tag

    @property
    def description(self) -> str:
        """
        Retrieves the description of the article.
        """
        return self._get_basetype_from_data('description', str)

    @property
    def seo_title(self) -> str:
        """
        Retrieves the SEO title of the article.
        """
        return self._get_basetype_from_data('seoTitle', str)

    @property
    def title(self) -> str:
        """
        Retrieves the title of the article.
        """
        return self._get_basetype_from_data('title', str)

    @property
    def article_id(self) -> str:
        """
        Retrieves the ID of the article.
        """
        return self._get_basetype_from_data('_id', str)

    @property
    def slug(self) -> str:
        """
        Retrieves the slug of the article.
        """
        return self._get_basetype_from_data('slug', str)

    @staticmethod
    async def from_records(session: ClientSession, new_data: dict) -> 'Article':
        """
        Creates an Article instance from records.
        """
        new_article = Article(session=session)
        new_article._update_data(new_data)

        return new_article

    def __hash__(self) -> int:
        """
        Returns the hash value of the Article object.
        """
        return hash(self.article_id or self.slug)
