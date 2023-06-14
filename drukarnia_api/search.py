import asyncio
from typing import Iterable

from drukarnia_api.connection.connection import Connection

from drukarnia_api.author import Author
from drukarnia_api.article import Article
from drukarnia_api.tags import Tag


class Search(Connection):
    async def search_articles(self, query: str, create_articles: bool = True, offset: int = 0,
                              results_per_page: int = 20, n_collect: int = None,
                              *args, **kwargs) -> Iterable['Article']:

        request_url = '/api/articles/search?name={query}'.format(query=query)

        # Make a request to get the followers of the author
        articles = await self.multi_page_request(request_url, offset, results_per_page, n_collect, *args, **kwargs)

        if create_articles:
            # Create Author objects for each follower and store them in self.followers
            articles = await asyncio.gather(*[
                Article.from_records(self.session, **article) for article in articles
            ])

        return articles

    async def search_authors(self, query: str, create_authors: bool = True, offset: int = 0,
                             results_per_page: int = 20, n_collect: int = None, relations: bool = False,
                             *args, **kwargs) -> Iterable['Author']:

        request_url = '/api/users/info?name={query}&' \
                      'withRelationships={relations}'.format(query=query, relations=str(relations).lower())

        # Make a request to get the followers of the author
        authors = await self.multi_page_request(request_url, offset, results_per_page, n_collect, *args, **kwargs)

        if create_authors:
            # Create Author objects for each follower and store them in self.followers
            authors = await asyncio.gather(*[
                Author.from_records(self.session, **author) for author in authors
            ])

        return authors

    async def search_tags(self, query: str, create_tags: bool = True, offset: int = 0,
                          results_per_page: int = 20, n_collect: int = None, *args, **kwargs) -> Iterable['Tag']:

        request_url = '/api/articles/search/tags?text={query}'.format(query=query)

        # Make a request to get the followers of the author
        tags = await self.multi_page_request(request_url, offset, results_per_page, n_collect, *args, **kwargs)

        if create_tags:
            # Create Author objects for each follower and store them in self.followers
            tags = await asyncio.gather(*[
                Tag.from_records(self.session, **tag) for tag in tags
            ])

        return tags
