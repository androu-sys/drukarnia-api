import asyncio

from aiohttp import ClientSession
from drukarnia_api.drukarnia_base.element import DrukarniaElement

from drukarnia_api.shortcuts.class_generator import data2authors, data2articles  # data2tags


class Article(DrukarniaElement):
    def __init__(self, slug: str = None, article_id: str = None, *args, **kwargs):
        """
        Initializes an Article object with the given slug and article ID.
        """
        super().__init__(*args, **kwargs)

        self._update_data({'slug': slug, '_id': article_id})

    @DrukarniaElement._is_authenticated
    async def post_comment(self, comment_text: str) -> str:
        """
        Posts a comment on the article and returns the ID of the posted comment.
        """
        self._control_attr('article_id')

        posted_comment_id = await self.post('/api/articles/{_id}/comments'.format(_id=self.article_id),
                                            {'comment': comment_text}, output='read')
        return str(posted_comment_id)

    @DrukarniaElement._is_authenticated
    async def reply2comment(self, comment_text: str, comment_id: str, root_comment: str,
                            root_comment_owner: str, reply2user: str) -> str:
        """
        Posts a reply to a comment and returns the ID of the new comment.
        """
        self._control_attr('article_id')

        new_comment_id = await self.post(
            f'/api/articles/{self.article_id}/comments/{comment_id}/replies',
            {
                "comment": comment_text, "replyToComment": comment_id, "rootComment": root_comment,
                "rootCommentOwner": root_comment_owner, "replyToUser": reply2user
            },
            output='read'
        )

        return str(new_comment_id)

    @DrukarniaElement._is_authenticated
    async def delete_comment(self, comment_id: str) -> None:
        """
        Deletes a comment from the article.
        """
        self._control_attr('article_id')

        await self.delete(f'/api/articles/{self.article_id}/comments/{comment_id}', [])

    @DrukarniaElement._is_authenticated
    async def like_comment(self, comment_id: str, delete: bool = False) -> None:
        """
        Likes or unlikes a comment based on the 'delete' parameter.
        """
        self._control_attr('article_id')

        if delete:
            await self.delete(f'/api/articles/{self.article_id}/comments/{comment_id}/likes', [])
        else:
            await self.post(f'/api/articles/{self.article_id}/comments/{comment_id}/likes', {}, [])

    @DrukarniaElement._is_authenticated
    async def like_article(self, n_likes: int) -> None:
        """
        Likes the article with the specified number of likes.
        """
        self._control_attr('article_id')

        if not (0 <= n_likes <= 10):
            raise ValueError('Number of likes must be greater or equal to zero and lower or equal to ten')

        await self.post(f'/api/articles/{self.article_id}/like', {'likes': n_likes}, 'read')

    @DrukarniaElement._is_authenticated
    async def bookmark(self, section_id: str = '', unbookmark: bool = False) -> None:
        """
        Adds or removes the article from bookmarks based on the 'unbookmark' parameter.
        """
        self._control_attr('article_id')

        if unbookmark:
            await self.delete(f'/api/articles/{self.article_id}/bookmarks', [])
        elif not section_id:
            raise ValueError('section_id must be passed to bookmark')
        else:
            await self.post('/api/articles/bookmarks', {"article": self.article_id, "list": section_id}, [])

    async def collect_data(self, return_: bool = False) -> dict or None:
        """
        Collects the article's data and updates the object's attributes.
        If 'return_' is True, returns the collected data.
        """
        self._control_attr('slug')

        data = await self.get(f'/api/articles/{self.slug}', output='json')

        self._update_data(data)

        if return_:
            return data

    @staticmethod
    async def from_records(session: ClientSession, new_data: dict) -> 'Article':
        """
        Creates an Article instance from records.
        """
        new_article = Article(session=session)
        new_article._update_data(new_data)

        return new_article

    @property
    async def owner(self):
        """
        Retrieves the owner of the article.
        """
        owner = self._access_data('owner', None)
        if owner is None:
            return None

        return await data2authors([owner], self.session)

    @property
    def comments(self):
        """
        Retrieves the comments of the article.
        """
        return self._access_data('comments', list)

    @property
    async def recommended_articles(self):
        """
        Retrieves the recommended articles related to the article.
        """
        return await data2articles(self._access_data('recommendedArticles', []), self.session)

    @property
    def relationships(self):
        """
        Retrieves the relationships of the article.
        """
        return self._get_basetype_from_author_data('relationships', dict)

    @property
    @DrukarniaElement._is_authenticated
    def is_bookmarked(self):
        """
        Checks if the article is bookmarked.
        """
        return self._get_basetype_from_author_data('isBookmarked', bool)

    @property
    @DrukarniaElement._is_authenticated
    def is_liked(self):
        """
        Checks if the article is liked.
        """
        return self._get_basetype_from_author_data('isLiked', bool)

    @property
    def sensitive(self):
        """
        Checks if the article is sensitive.
        """
        return self._get_basetype_from_author_data('sensitive', bool)

    @property
    def content(self):
        """
        Retrieves the content of the article.
        """
        return self._get_basetype_from_author_data('content', dict)

    @property
    async def author_articles(self):
        """
        Retrieves the articles written by the author of the article.
        """
        return await data2articles(self._access_data('authorArticles', []), self.session)

    @property
    def thumb_picture(self):
        """
        Retrieves the thumbnail picture of the article.
        """
        return self._get_basetype_from_author_data('thumbPicture', str)

    @property
    def picture(self):
        """
        Retrieves the picture of the article.
        """
        return self._get_basetype_from_author_data('picture', str)

    @property
    def ads(self):
        """
        Retrieves the ads of the article.
        """
        return self._get_basetype_from_author_data('ads', str)

    @property
    def index(self):
        """
        Retrieves the index of the article.
        """
        return self._get_basetype_from_author_data('index', str)

    @property
    def created_at(self):
        """
        Retrieves the creation date of the article.
        """
        return self._get_datetime_from_author_data('createdAt')

    @property
    def read_time(self):
        """
        Retrieves the read time of the article.
        """
        return self._get_basetype_from_author_data('readTime', float)

    @property
    def number_of_like(self):
        """
        Retrieves the number of likes of the article.
        """
        return self._get_basetype_from_author_data('description', int)

    @property
    def number_of_comment(self):
        """
        Retrieves the number of comments of the article.
        """
        return self._get_basetype_from_author_data('commentNum', int)

    @property
    def article_tags(self):
        """
        Retrieves the tags of the article.
        """
        return self._get_basetype_from_author_data('tags', dict)

    @property
    def main_article_tag(self):
        """
        Retrieves the main tag of the article.
        """
        return self._get_basetype_from_author_data('mainTag', str)

    @property
    def description(self):
        """
        Retrieves the description of the article.
        """
        return self._get_basetype_from_author_data('description', str)

    @property
    def seo_title(self):
        """
        Retrieves the SEO title of the article.
        """
        return self._get_basetype_from_author_data('seoTitle', str)

    @property
    def title(self):
        """
        Retrieves the title of the article.
        """
        return self._get_basetype_from_author_data('title', str)

    @property
    def article_id(self):
        """
        Retrieves the ID of the article.
        """
        return self._get_basetype_from_author_data('_id', str)

    @property
    def slug(self):
        """
        Retrieves the slug of the article.
        """
        return self._get_basetype_from_author_data('slug', str)

    def __hash__(self):
        """
        Returns the hash value of the Article object.
        """
        return hash(self.article_id or self.slug)


if __name__ == '__main__':
    import pprint
    from drukarnia_api.author import Author
    author = Author('digitalowltop')

    loop = asyncio.get_event_loop()
    # loop.run_until_complete(author.login('08gilts_slates@icloud.com', 'xamjeb-Forjac-8rafzI'))

    loop.run_until_complete(author.collect_data())
    first_article = loop.run_until_complete(author.articles)[0]

    loop.run_until_complete(first_article.collect_data())
    pprint.pprint(author.all_collected_data)

    loop.run_until_complete(author.close_session())
