from typing import Tuple
from aiohttp import ClientSession
import asyncio


async def data2tags(tags_data: list or None, session: ClientSession) -> Tuple:
    """
    Converts a list of tag data into Tag objects asynchronously.

    Args:
        tags_data (list or None): List of tag data.
        session (ClientSession): aiohttp ClientSession object.

    Returns:
        Tuple: Tuple of Tag objects.
    """
    if not tags_data:
        return ()

    from drukarnia_api.tag import Tag

    tasks = [Tag.from_records(session, tag) for tag in tags_data]

    return await asyncio.gather(*tasks)


async def data2authors(authors_data: list or None, session: ClientSession) -> Tuple:
    """
    Converts a list of author data into Author objects asynchronously.

    Args:
        authors_data (list or None): List of author data.
        session (ClientSession): aiohttp ClientSession object.

    Returns:
        Tuple: Tuple of Author objects.
    """
    if not authors_data:
        return ()

    from drukarnia_api.author import Author

    tasks = [Author.from_records(session, author) for author in authors_data]

    return await asyncio.gather(*tasks)


async def data2articles(articles_data: list or None, session: ClientSession) -> Tuple:
    """
    Converts a list of article data into Article objects asynchronously.

    Args:
        articles_data (list or None): List of article data.
        session (ClientSession): aiohttp ClientSession object.

    Returns:
        Tuple: Tuple of Article objects.
    """
    if not articles_data:
        return ()

    from drukarnia_api.article import Article

    tasks = [Article.from_records(session, article) for article in articles_data]

    return await asyncio.gather(*tasks)
