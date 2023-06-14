import asyncio
from warnings import warn

from aiohttp import ClientSession
from drukarnia_api.connection.connection import Connection
from inspect import currentframe


class Article(Connection):
    def __init__(self, slug: str = None, _id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id
        self.slug = slug
        self.title = None
        self.seoTitle = None
        self.description = None
        self.picture = None
        self.mainTag = None
        self.tags = None
        self.index = None
        self.sensitive = None
        self.likeNum = None
        self.commentNum = None
        self.readTime = None
        self.mainTagSlug = None
        self.mainTagId = None
        self.createdAt = None
        self.thumbPicture = None
        self.authorArticles = None
        self.content = None
        self.isLiked = None
        self.owner = None
        self.isBookmarked = None
        self.relationships = None
        self.recommendedArticles = None
        self.comments = None

    async def is_authenticated(self):
        if not self.session.headers.get('Cookie', None):
            warn('We were not able to locate cookie files in your session data. It may cause errors for'
                 ' this function. Provide your own header with cookies or user Author.login before creat'
                 'ing Article object')

    async def control_params(self, *args) -> None:
        """
        Validate the required fields for processing a specific method.
        """

        calling_by = currentframe().f_back.f_code.co_name

        for name in args:
            if not self.__dict__.get(name, None):
                raise ValueError(f'field {name} is required to process {calling_by}. Usually required data can be'
                                 f'obtained by calling collect_data method first.')

    async def post_comment(self, comment_text: str) -> str:

        """example of comment_text: <p>Дякую, <strong>дуже</strong> цікаво<em>!</em></p>"""

        await self.control_params('_id')
        await self.is_authenticated()

        request_url = '/api/articles/{_id}/comments'.format(_id=self._id)

        posted_comment_id = await self.post(request_url, {'comment': comment_text}, 'read')
        return str(posted_comment_id)

    async def reply2comment(self, comment_id: str, rootComment: str, rootCommentOwner: str, replyToUser: str) -> str:
        await self.control_params('_id')
        await self.is_authenticated()

        request_url = '/api/articles/{_id}/comments/{comment_id}/replies'.format(_id=self._id, comment_id=comment_id)
        data = {"comment": "❤️", "replyToComment": comment_id, "rootComment": rootComment,
                "rootCommentOwner": rootCommentOwner, "replyToUser": replyToUser}

        posted_comment_id = await self.post(request_url, data, 'read')
        return str(posted_comment_id)

    async def delete_comment(self, comment_id: str) -> None:
        await self.control_params('_id')
        await self.is_authenticated()

        request_url = '/api/articles/{_id}/comments/{comment_id}'.format(_id=self._id, comment_id=comment_id)

        await self.delete(request_url, [])

    async def like_comment(self, comment_id: str, delete: bool = False) -> None:
        await self.control_params('_id')
        await self.is_authenticated()

        request_url = '/api/articles/{_id}/comments/{comment_id}/likes'.format(_id=self._id, comment_id=comment_id)

        if delete:
            await self.delete(request_url, [])

        else:
            await self.post(request_url, {}, [])

    async def like_article(self, n_likes: int) -> None:
        await self.control_params('_id')
        await self.is_authenticated()

        request_url = '/api/articles/{_id}/like'.format(_id=self._id)

        await self.post(request_url, {'likes': n_likes}, 'read')

    async def bookmark(self, section_id: str) -> None:
        await self.control_params('_id')
        await self.is_authenticated()

        await self.post('/api/articles/bookmarks', {"article": self._id, "list": section_id}, [])

    async def unbookmark(self) -> None:
        await self.control_params('_id')
        await self.is_authenticated()

        await self.delete(f'/api/articles/{self._id}/bookmarks', [])

    async def collect_data(self, return_: bool = False) -> dict or None:
        """
        Collect the article's data and update the object's attributes.
        """

        await self.control_params('slug')

        request_url = '/api/articles/{slug}'.format(slug=self.slug)

        data = await self.get(request_url, output='json')
        self.__dict__ = {key: data.get(key, value)
                         for key, value in self.__dict__.items()}

        if return_:
            return data

    async def create_article(self, *args, **kwargs) -> 'Article':

        pass

        ## TODO

    @staticmethod
    async def from_records(session: ClientSession, **kwargs) -> 'Article':
        """
        Create an Article instance from records.
        """

        new_article = Article(session=session)
        new_article.__dict__ = {key: kwargs.get(key, value)
                                for key, value in new_article.__dict__.items()}

        return new_article

    def __hash__(self):
        return hash(self._id or self.slug)


if __name__ == '__main__':
    from drukarnia_api.author import Author
    author = Author('grinch')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(author.login('08gilts_slates@icloud.com', 'xamjeb-Forjac-8rafzI'))

    article = Article(session=author.session, _id='648614fe280f442102d35859')

    print(loop.run_until_complete(article.like_article(5)))

