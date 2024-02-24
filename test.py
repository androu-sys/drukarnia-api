import aiohttp


async def get_author_article_titles():

    async with aiohttp.ClientSession() as session:
        response = await session.get(
            url="https://drukarnia.com.ua/api/users/profile/mantis"
        )
        return print(await response.json())


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_author_article_titles())