from drukarnia_api.connection import GetRequest
from urllib.parse import quote
import asyncio

from aiohttp import ClientSession


class Article:
    session = None
    data = None

    @staticmethod
    def find_article(session: ClientSession, name_slug: str) -> 'Article':
        url = '/api/articles/{name_slug}'.format(name_slug=quote(name_slug))

        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(GetRequest.get(session, url))

        article = Article()
        article.session, article.data = session, data

        return article
