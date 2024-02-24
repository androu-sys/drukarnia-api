from drukarnia_api import Search


async def get_author_article_titles():
    search = Search()

    async with search:
        search_res = await search.find_author('mantis')
        # most probable
        cupomanka = search_res[0]

        # Collect all data about the user
        await cupomanka.collect_data()
        print(cupomanka.data)


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_author_article_titles())
