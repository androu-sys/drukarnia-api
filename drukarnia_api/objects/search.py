from drukarnia_api.objects.base_object import DrukarniaElement
from drukarnia_api.shortcuts import data2authors, data2articles, data2tags

from typing import TYPE_CHECKING, Tuple, Dict

if TYPE_CHECKING:
    from drukarnia_api.objects.article import Article
    from drukarnia_api.objects.tag import Tag
    from drukarnia_api.objects.author import Author


class Search(DrukarniaElement):
    async def find_author(self,
                          query: str,
                          create_authors: bool = True,
                          with_relations: bool = False,
                          offset: int = 0,
                          results_per_page: int = 20,
                          n_collect: int = None,
                          *args, **kwargs) -> Tuple['Author'] or Tuple[Dict]:
        """
        Search for authors.

        Parameters:
        - query (str): The search query for authors.
        - create_authors (bool, optional): Whether to create author objects from the search results. Defaults to True.
        - with_relations (bool, optional): Whether to include author relationships in the search results.
         Defaults to False.
        - offset (int, optional): The starting index of the search results. Defaults to 0.
        - results_per_page (int, optional): The maximum number of authors to be returned per page. Defaults to 20.
        - n_collect (int, optional): The total number of authors to be collected. Defaults to None.

        Returns:
        - Tuple['Author'] or Tuple[Dict]: A tuple containing a list of
        Author objects or a dictionary representing the search results.
        """

        with_relations = str(with_relations).lower()

        # Make a request to get authors
        authors = await self.multi_page_request(f'/api/users/info?name={query}&withRelationships={with_relations}',
                                                offset, results_per_page, n_collect, *args, **kwargs)

        if create_authors:
            authors = await data2authors(authors, self.session)

        return authors

    async def find_articles(self,
                            query: str,
                            create_articles: bool = True,
                            offset: int = 0,
                            results_per_page: int = 20,
                            n_collect: int = None,
                            *args, **kwargs) -> Tuple['Article'] or Tuple[Dict]:
        """
        Search for articles.

        Parameters:
        - query (str): The search query for articles.
        - create_articles (bool, optional): Whether to create article objects from the search results. Defaults to True.
        - offset (int, optional): The starting index of the search results. Defaults to 0.
        - results_per_page (int, optional): The maximum number of articles to be returned per page. Defaults to 20.
        - n_collect (int, optional): The total number of articles to be collected. Defaults to None.

        Returns:
        - Tuple['Article'] or Tuple[Dict]: A tuple containing a list of
        Article objects or a dictionary representing the search results.
        """

        # Make a request to get articles
        articles = await self.multi_page_request(f'/api/articles/search?name={query}',
                                                 offset, results_per_page, n_collect, *args, **kwargs)

        if create_articles:
            articles = await data2articles(articles, self.session)

        return articles

    async def find_tags(self,
                        query: str,
                        create_tags: bool = True,
                        offset: int = 0,
                        results_per_page: int = 20,
                        n_collect: int = None, **kwargs) -> Tuple['Tag'] or Tuple[Dict]:
        """
        Search for tags.

        Parameters:
        - query (str): The search query for tags.
        - create_tags (bool, optional): Whether to create tag objects from the search results. Defaults to True.
        - offset (int, optional): The starting index of the search results. Defaults to 0.
        - results_per_page (int, optional): The maximum number of tags to be returned per page. Defaults to 20.
        - n_collect (int, optional): The total number of tags to be collected. Defaults to None.
        - **kwargs: Additional keyword arguments to pass to the search API.

        Returns:
        - Tuple['Tag'] or Tuple[Dict]: A tuple containing a list of Tag objects or
         a dictionary representing the search results.
        """

        # Make a request to get articles
        tags = await self.multi_page_request(
            f'/api/articles/search/tags?text={query}',
            key='tags',
            offset=offset,
            results_per_page=results_per_page,
            n_collect=n_collect, **kwargs
        )

        if create_tags:
            tags = await data2tags(tags, self.session)

        return tags
