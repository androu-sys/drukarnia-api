from drukarnia_api.drukarnia_base import Connection
from drukarnia_api.shortcuts import data2authors, data2articles, data2tags

from typing import TYPE_CHECKING, Tuple, Dict

if TYPE_CHECKING:   # always False, used for type hints
    from drukarnia_api.article import Article
    from drukarnia_api.tag import Tag
    from drukarnia_api.author import Author


class Search(Connection):
    async def find_author(self, query: str, create_authors: bool = True, with_relations: bool = False,
                          offset: int = 0, results_per_page: int = 20, n_collect: int = None,
                          *args, **kwargs) -> Tuple['Author'] or Tuple[Dict]:
        """
        Search for authors.
        """

        with_relations = str(with_relations).lower()

        # Make a request to get authors
        authors = await self.multi_page_request(f'/api/users/info?name={query}&withRelationships={with_relations}',
                                                offset, results_per_page, n_collect, *args, **kwargs)

        if create_authors:
            authors = await data2authors(authors, self.session)

        return authors

    async def find_articles(self, query: str, create_articles: bool = True,
                            offset: int = 0, results_per_page: int = 20, n_collect: int = None,
                            *args, **kwargs) -> Tuple['Article'] or Tuple[Dict]:
        """
        Search for articles.
        """

        # Make a request to get articles
        articles = await self.multi_page_request(f'/api/articles/search?name={query}',
                                                 offset, results_per_page, n_collect, *args, **kwargs)

        if create_articles:
            articles = await data2articles(articles, self.session)

        return articles

    async def find_tags(self, query: str, create_tags: bool = True,
                        offset: int = 0, results_per_page: int = 20, n_collect: int = None,
                        *args, **kwargs) -> Tuple['Tag'] or Tuple[Dict]:
        """
        Search for tags.
        """

        # Make a request to get articles
        tags = await self.multi_page_request(f'/api/articles/search/tags?text={query}',
                                             offset, results_per_page, n_collect, *args, **kwargs)

        if create_tags:
            tags = await data2tags(tags, self.session)

        return tags
