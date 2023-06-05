import asyncio

from aiohttp import ClientSession
from fake_useragent import UserAgent

from time import sleep
from random import random

from typing import List, Any, Generator, Iterable, Dict, Callable


class Connection:
    base_url = 'https://drukarnia.com.ua'

    def __init__(self, session: ClientSession = None, headers: dict = None,
                 create_user_agent: bool = True, random_sleep: bool = True,
                 sleep_range: float = 0.3, *args, **kwargs):

        """
        Initializes a Connection object.
        """

        if session:
            self.session = session

        else:
            if headers is None:
                headers = {}

            if create_user_agent:
                headers['User-Agent'] = UserAgent().random

            self.session = ClientSession(base_url=self.base_url, headers=headers, *args, **kwargs)

        if random_sleep:
            self.random_sleep = lambda: sleep(random() * sleep_range)

        else:
            self.random_sleep = lambda: None

    async def get_json(self, url: str, params: dict = None,
                       include_header: bool = False, *args, **kwargs) -> dict or tuple:

        """
        Sends a GET request and retrieves JSON data.

        """

        print(url, params)

        self.random_sleep()

        async with self.session.get(url, params=params, *args, **kwargs) as response:
            result = await response.json()

            if ('statusCode' in result) and (result['statusCode'] != 200):
                raise ValueError("Drukarnia API error - '{}'".format(result['message']))

            elif include_header:
                return result, response.headers

            return result

    async def post_json(self, url: str, data: dict = None,
                        include_header: bool = False, *args, **kwargs) -> dict or tuple:

        """
        Sends a GET request and retrieves JSON data.
        """

        self.random_sleep()

        async with self.session.post(url, data=data, **kwargs) as response:
            result = await response.json()

            if ('statusCode' in result) and (result['statusCode'] != 200):
                raise ValueError("Drukarnia API error - '{}'".format(result['message']))

            elif include_header:
                return result, response.headers

            return result

    async def get_pool(self, heuristics: Iterable[dict]):

        """
        Sends multiple GET requests concurrently.
        """

        # create tasks
        tasks = [self.get_json(**kwargs) for kwargs in heuristics]

        # get results
        return await asyncio.gather(*tasks)

    async def run_until_no_stop(self, request_synthesizer: Generator[Dict, None, None],
                                not_stop_until: Callable[[Any], bool], n_results: int = None,
                                batch_size: int = 5) -> List[Any]:

        """
        Drukarnia API uses 'page' parameter for pagination instead of more common
        start/offset, so this function simplifies the scraping of multipage calls, like followers,
        articles, notifications and many others
        """

        all_results = []
        step = 0

        while True:
            heuristics = [next(request_synthesizer) for _ in range(step, step+batch_size)]

            if n_results is not None:
                heuristics = heuristics[:n_results]
                n_results -= batch_size

            _results = await self.get_pool(heuristics=heuristics)
            responses = [_result for _result in _results if not_stop_until(_result)]

            all_results.extend(responses)
            step += batch_size

            if len(responses) != batch_size:
                break

        return all_results

    async def multi_page_request(self, direct_url: str, offset: int = 0, results_per_page: int = 20,
                                 n_collect: int = None, *args, **kwargs):
        """this is the shortcut for using run_until_no_stop for multi_page_scraping,
        I really hope Drukarnia API will depricate this page-system and replace it with normal offset/pages params."""

        if offset < 0:
            raise ValueError('offset must be greater or equall to one')

        elif n_collect and n_collect < 1:
            raise ValueError('n_collect must be greater or equall to one')

        def synthesizer():
            start_page = offset // results_per_page + 1

            while True:
                yield {'url': direct_url, 'params': {'page': start_page}}
                start_page += 1

        data = await self.run_until_no_stop(request_synthesizer=synthesizer(),
                                            not_stop_until=lambda result: result != [],
                                            n_results=n_collect // results_per_page + 1 if n_collect else None,
                                            *args, **kwargs)

        records = [record for page in data for record in page]

        adjusted_start = offset % results_per_page

        if n_collect:
            return records[adjusted_start:adjusted_start+n_collect]

        return records[adjusted_start:]

    def __del__(self):
        asyncio.run(
            self.session.close()
        )
