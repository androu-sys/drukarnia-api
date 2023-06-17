import asyncio

from aiohttp import ClientSession
from drukarnia_api.drukarnia_base.element import DrukarniaElement

from drukarnia_api.shortcuts.class_generator import data2authors, data2articles  # data2tags


class Article(DrukarniaElement):
    def __init__(self, slug: str = None, article_id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._update_data({'slug': slug, '_id': article_id})

    @DrukarniaElement._is_authenticated
    async def post_comment(self, comment_text: str) -> str:
        self._control_attr('article_id')

        posted_comment_id = await self.post('/api/articles/{_id}/comments'.format(_id=self.article_id),
                                            {'comment': comment_text}, output='read')
        return str(posted_comment_id)

    @DrukarniaElement._is_authenticated
    async def reply2comment(self, comment_text: str, comment_id: str, root_comment: str,
                            root_comment_owner: str, reply2user: str) -> str:
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
        self._control_attr('article_id')

        await self.delete(f'/api/articles/{self.article_id}/comments/{comment_id}', [])

    @DrukarniaElement._is_authenticated
    async def like_comment(self, comment_id: str, delete: bool = False) -> None:
        self._control_attr('article_id')

        if delete:
            await self.delete(f'/api/articles/{self.article_id}/comments/{comment_id}/likes', [])

        else:
            await self.post(f'/api/articles/{self.article_id}/comments/{comment_id}/likes', {}, [])

    @DrukarniaElement._is_authenticated
    async def like_article(self, n_likes: int) -> None:
        self._control_attr('article_id')

        if not (0 <= n_likes <= 10):
            raise ValueError('Number of likes must be greater or equall to zero and lower or equall to ten')

        await self.post(f'/api/articles/{self.article_id}/like', {'likes': n_likes}, 'read')

    @DrukarniaElement._is_authenticated
    async def bookmark(self, section_id: str = '', unbookmark: bool = False) -> None:
        self._control_attr('article_id')

        if unbookmark:
            await self.delete(f'/api/articles/{self.article_id}/bookmarks', [])

        elif not section_id:
            raise ValueError('section_id must be passed to bookmark')

        else:
            await self.post('/api/articles/bookmarks', {"article": self.article_id, "list": section_id}, [])

    async def collect_data(self, return_: bool = False) -> dict or None:
        """
        Collect the article's data and update the object's attributes.
        """
        self._control_attr('slug')

        data = await self.get(f'/api/articles/{self.slug}', output='json')

        self._update_data(data)

        if return_:
            return data

    @staticmethod
    async def from_records(session: ClientSession, new_data: dict) -> 'Article':
        """
        Create an Article instance from records.
        """

        new_article = Article(session=session)
        new_article._update_data(new_data)

        return new_article

    @property
    async def owner(self):
        owner = self._access_data('owner', None)
        if owner is None:
            return None

        return await data2authors([owner], self.session)

    @property
    def comments(self):
        return self._access_data('comments', list)

    @property
    async def recommended_articles(self):
        return await data2articles(self._access_data('recommendedArticles', []), self.session)

    @property
    def relationships(self):
        return self._get_basetype_from_author_data('relationships', dict)

    @property
    @DrukarniaElement._is_authenticated
    def is_bookmarked(self):
        return self._get_basetype_from_author_data('isBookmarked', bool)

    @property
    @DrukarniaElement._is_authenticated
    def is_liked(self):
        return self._get_basetype_from_author_data('isLiked', bool)

    @property
    def sensitive(self):
        return self._get_basetype_from_author_data('sensitive', bool)

    @property
    def content(self):
        return self._get_basetype_from_author_data('content', dict)

    @property
    async def author_articles(self):
        return await data2articles(self._access_data('authorArticles', []), self.session)

    @property
    def thumb_picture(self):
        return self._get_basetype_from_author_data('thumbPicture', str)

    @property
    def picture(self):
        return self._get_basetype_from_author_data('picture', str)

    @property
    def ads(self):
        return self._get_basetype_from_author_data('ads', str)

    @property
    def index(self):
        return self._get_basetype_from_author_data('index', str)

    @property
    def created_at(self):
        return self._get_datetime_from_author_data('createdAt')

    @property
    def read_time(self):
        return self._get_basetype_from_author_data('readTime', float)

    @property
    def like_num(self):
        return self._get_basetype_from_author_data('description', int)

    @property
    def comment_num(self):
        return self._get_basetype_from_author_data('commentNum', int)

    @property
    def article_tags(self):
        # await data2tags(self._access_data('tags', []), self.session)
        return self._get_basetype_from_author_data('tags', dict)

    @property
    def main_article_tag(self):
        # mainTag, mainTagSlug, mainTagId,
        return self._get_basetype_from_author_data('mainTag', str)

    @property
    def description(self):
        return self._get_basetype_from_author_data('description', str)

    @property
    def seo_title(self):
        return self._get_basetype_from_author_data('seoTitle', str)

    @property
    def title(self):
        return self._get_basetype_from_author_data('title', str)

    @property
    def article_id(self):
        return self._get_basetype_from_author_data('_id', str)

    @property
    def slug(self):
        return self._get_basetype_from_author_data('slug', str)

    def __hash__(self):
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
