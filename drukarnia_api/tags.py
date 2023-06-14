import asyncio
from typing import Iterable
from warnings import warn

from aiohttp import ClientSession
from drukarnia_api.connection.connection import Connection
from inspect import currentframe


class Tag(Connection):
    def __init__(self, name: str = None, _id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id
        self.name = name

    async def control_params(self, *args) -> None:
        """
        Validate the required fields for processing a specific method.
        """

        calling_by = currentframe().f_back.f_code.co_name

        for name in args:
            if not self.__dict__.get(name, None):
                raise ValueError(f'field {name} is required to process {calling_by}. Usually required data can be'
                                 f'obtained by calling collect_data method first.')

    async def subscribe(self) -> None:
        await self.is_authenticated()

        request_url = '/api/preferences/tags/{_id}'.format(_id=self._id)

        await self.put(request_url, None, [])

    async def unsubscribe(self) -> None:
        await self.is_authenticated()

        request_url = '/api/preferences/tags/{_id}'.format(_id=self._id)

        await self.delete(request_url, [])

    async def block(self, unblock: bool = False) -> dict:
        await self.is_authenticated()

        request_url = '/api/preferences/tags/{_id}/block'.format(_id=self._id)

        return await self.put(request_url, {'isBlocked': not unblock}, 'json')

    async def get_articles(self, offset: int = 0, results_per_page: int = 20,
                           n_collect: int = None, *args, **kwargs) -> Iterable:
        """
        Get the followers of the author.
        """

        await self.control_params('_id')

        request_url = '/api/articles/tags/{name}'.format(name=self.name)

        # Make a request to get the followers of the author
        articles = await self.multi_page_request(request_url, offset, results_per_page, n_collect, *args, **kwargs)

        return articles

    @staticmethod
    async def from_records(session: ClientSession, **kwargs) -> 'Tag':
        """
        Create an Author instance from records.
        """

        new_tag = Tag(session=session)
        new_tag.__dict__ = {key: kwargs.get(key, value)
                            for key, value in new_tag.__dict__.items()}

        return new_tag

    def __hash__(self):
        return hash(self._id or self.name)
