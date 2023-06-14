import re
from typing import Iterable, Any
import asyncio
from aiohttp import ClientSession
from drukarnia_api.connection import Connection
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

    async def control_params(self, *args) -> None:
        """
        Validate the required fields for processing a specific method.
        """

        calling_by = currentframe().f_back.f_code.co_name

        for name in args:
            if not self.__dict__.get(name, None):
                raise ValueError(f'field {name} is required to process {calling_by}. Usually required data can be'
                                 f'obtained by calling collect_data method first.')

    async def like(self, n_likes: int) -> None:
        await self.control_params('_id')

        request_url = '/api/articles/{_id}/like'.format(_id=self._id)

        return await self.post(request_url, {'likes': n_likes}, 'read')

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