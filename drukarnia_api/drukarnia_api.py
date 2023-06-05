from aiohttp import ClientSession
from fake_useragent import UserAgent

from drukarnia_api.author import Author
from drukarnia_api.connection import Connection

from typing import Iterable


class DrukarniaAPI:
    base_url = 'https://drukarnia.com.ua'

    def __init__(self, password: str = None, email: str = None, session: ClientSession = None):
        if session:
            self.session = session

        else:
            headers = {'User-Agent': UserAgent().random}

            if password and email:
                headers |= {'email': email, 'password': password}

            self.session = ClientSession(base_url=self.base_url, headers=headers)

    async def search_authors(self, query: str, with_relationships: bool = False,
                             create_authors: bool = True, *args, **kwargs) -> Iterable['Author']:
        # Create a request URL to search for authors based on a query and relationship option
        request_url = '/api/users/info'
        params = {'name': query, 'withRelationships': with_relationships, 'page': }

        # Make a request to search for authors
        results = await (session, request_url, *args, **kwargs)

        if create_authors:
            # Create Author objects for each search result and return them as a list
            results = [Author(session, data=result) for result in results]

        return results
