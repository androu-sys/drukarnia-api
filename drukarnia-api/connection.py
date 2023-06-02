import asyncio

from aiohttp import ClientSession
from typing import List


class GetRequest:
    @staticmethod
    async def get(session: ClientSession, url: str):

        async with session.get(url) as response:
            result = await response.json()

            if ('statusCode' in result) and (result['statusCode'] != 200):
                raise ValueError("{}".format(result['message']))

            return result

    @staticmethod
    async def get_pool(session: ClientSession, urls: List[str]):
        # create tasks
        tasks = [GetRequest.get(session, url)
                 for url in urls]

        # get results
        return await asyncio.gather(*tasks)
