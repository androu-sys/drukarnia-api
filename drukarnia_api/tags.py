from typing import Iterable
from aiohttp import ClientSession
from drukarnia_api.connection.connection import Connection


class Tag(Connection):
    def __init__(self, name: str = None, _id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id
        self.name = name

    async def _control_attr(self, attr: str) -> None:
        if getattr(self, attr) is None:
            raise ValueError(f'{attr} is required. If you don\'t now it, call collect_data method before')

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

        await self._control_attr('_id')

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
