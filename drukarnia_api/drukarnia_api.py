from aiohttp import ClientSession
from fake_useragent import UserAgent

from drukarnia_api.author import Author
from drukarnia_api.article import Article


class DrukarniaAPI:
    base_url = 'https://drukarnia.com.ua'

    def __init__(self, session: ClientSession = None):

        if session:
            self.session = session

        else:
            headers = {'User-Agent': UserAgent().random}
            self.session = ClientSession(base_url=self.base_url, headers=headers)

    def get_author(self, username: str) -> 'Author':
        return Author.find_author(self.session, username)

    def get_article(self, name_slug: str) -> 'Article':
        return Article.find_article(self.session, name_slug)

    def __del__(self):
        from asyncio import get_event_loop

        loop = get_event_loop()
        loop.run_until_complete(
            self.session.close()
        )
