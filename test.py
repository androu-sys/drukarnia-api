import aiohttp


async def get_author_article_titles():
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            url="https://drukarnia.com.ua/api/users/login",
            data={"password": "Jondaw-popnu5-xatqev", "email": "a@gmail.com"},
        )
        print(await response.json())
        response = await session.patch(
            url="https://drukarnia.com.ua/api/users",
            data={"name": "HubaBuba2", "_id": "800e6363e31"},
        )
        print(await response.read())


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_author_article_titles())


# 65dad800e6363e315afa1a3a