import asyncio

from aiohttp import ClientSession
from fake_useragent import UserAgent

from typing import List, Any, Generator, Iterable, Dict


class Connection:
    base_url = 'https://drukarnia.com.ua'

    def __init__(self, session: ClientSession = None, headers: dict = None,
                 create_user_agent: bool = True, *args, **kwargs):

        """
        Initializes a Connection object.
        """

        if session:
            self.session = session
        else:
            if create_user_agent:
                headers['User-Agent'] = UserAgent().random

            self.session = ClientSession(base_url=self.base_url, headers=headers, *args, **kwargs)

    async def get_json(self, url: str, params: dict = None, *args, **kwargs) -> dict:

        """
        Sends a GET request and retrieves JSON data.
        """

        async with self.session.get(url, params=params, *args, **kwargs) as response:
            result = await response.json()

            if ('statusCode' in result) and (result['statusCode'] != 200):
                raise ValueError("{}".format(result['message']))

            return result

    async def get_pool(self, heuristics: Iterable[dict]):

        """
        Sends multiple GET requests concurrently.
        """

        # create tasks
        tasks = [self.get_json(**kwargs) for kwargs in heuristics]

        # get results
        return await asyncio.gather(*tasks)

    async def run_until_no_response(self, request_synthesizer: Generator[Dict, None, None],
                                    batch_size: int = 5) -> List[Any]:

        """
        Runs GET requests in batches until no response is received.
        """

        stop_action = lambda result: result == []

        all_results = []
        step = 0

        while True:
            heuristics = [next(request_synthesizer) for _ in range(step, step+batch_size)]

            _results = await self.get_pool(heuristics=heuristics)
            _results = [result for result in _results if stop_action(result)]
            all_results.extend(_results)

            step += batch_size

            if len(_results) != batch_size:
                break

        return all_results

    def __del__(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            self.session.close()
        )
