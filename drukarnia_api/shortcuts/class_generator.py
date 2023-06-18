import asyncio
from typing import Tuple

from aiohttp import ClientSession


async def data2tags(tags_data: list or None, session: ClientSession) -> Tuple:
    if not tags_data:
        return ()

    from drukarnia_api.tag import Tag

    tasks = [Tag.from_records(session, tag) for tag in tags_data]

    return await asyncio.gather(*tasks)


async def data2authors(authors_data: list or None, session: ClientSession) -> Tuple:
    if not authors_data:
        return ()

    from drukarnia_api.author import Author

    tasks = [Author.from_records(session, author) for author in authors_data]

    return await asyncio.gather(*tasks)


async def data2articles(articles_data: list or None, session: ClientSession) -> Tuple:
    if not articles_data:
        return ()

    from drukarnia_api.article import Article

    tasks = [Article.from_records(session, article) for article in articles_data]

    return await asyncio.gather(*tasks)
