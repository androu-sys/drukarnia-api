import asyncio
from aiohttp import ClientSession, ClientResponse, ContentTypeError
from fake_useragent import UserAgent
from typing import Any, Callable, Dict, Generator, Iterable, List
import inspect
from warnings import warn


async def _from_response(response: ClientResponse, output: str or List[str]) -> Any:
    """
    Extracts data from the response object based on the specified output format.
    """
    if isinstance(output, str):
        data = await _from_response(response, [output])
        return data[0]

    data = []
    for func_name in output:
        try:
            attr = getattr(response, func_name)

            if inspect.iscoroutinefunction(attr):
                data.append(await attr())

            elif callable(attr):
                data.append(attr())

            else:
                data.append(attr)

        except ContentTypeError as cte:
            warn('During calling {func_name} from response, '
                 'the following error occurred: \n{error}'.format(func_name=func_name, error=cte.message))

    return data


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
            if headers is None:
                headers = {}

            if create_user_agent:
                headers['User-Agent'] = UserAgent().random

            self.session = ClientSession(base_url=self.base_url, headers=headers, *args, **kwargs)

    async def get(self, url: str, params: dict = None,
                  output: str or list = 'json', *args, **kwargs) -> dict or tuple:
        """
        Sends a GET request and returns the response data based on the specified output format.
        """
        async with self.session.get(url, params=params, *args, **kwargs) as response:
            return await _from_response(response, output)

    async def patch(self, url: str, data: dict = None,
                    output: str or list = 'json', **kwargs) -> dict or tuple:
        """
        Sends a PATCH request and returns the response data based on the specified output format.
        """
        async with self.session.patch(url, data=data, **kwargs) as response:
            return await _from_response(response, output)

    async def post(self, url: str, data: dict = None,
                   output: str or list = 'json', **kwargs) -> dict or tuple:
        """
        Sends a POST request and returns the response data based on the specified output format.
        """
        async with self.session.post(url, data=data, **kwargs) as response:
            return await _from_response(response, output)

    async def delete(self, url: str, output: str or list = 'read', **kwargs):
        """
        Sends a DELETE request and returns the response data based on the specified output format.
        """
        async with self.session.delete(url, **kwargs) as response:
            return await _from_response(response, output)

    async def request_pool(self, heuristics: Iterable[dict]) -> Iterable:
        """
        Sends multiple GET requests concurrently.
        """
        # Create tasks
        tasks = [getattr(self, 'get')(**kwargs) if isinstance(kwargs, dict) else getattr(self, kwargs[1])(**kwargs[0])
                 for kwargs in heuristics]

        # Get results
        return await asyncio.gather(*tasks)

    async def run_until_no_stop(self, request_synthesizer: Generator[Dict or List[Dict, str], None, None],
                                not_stop_until: Callable[[Any], bool], n_results: int = None,
                                batch_size: int = 5) -> List[Any]:
        """
        Executes requests until the specified stopping condition is met,
        and returns the aggregated results.
        """
        all_results = []
        step = 0

        while True:
            heuristics = [next(request_synthesizer) for _ in range(step, step + batch_size)]

            if n_results is not None:
                heuristics = heuristics[:n_results]
                n_results -= batch_size

            _results = await self.request_pool(heuristics=heuristics)
            responses = [_result for _result in _results if not_stop_until(_result)]

            all_results.extend(responses)
            step += batch_size

            if len(responses) != batch_size:
                break

        return all_results

    async def multi_page_request(self, direct_url: str, offset: int = 0, results_per_page: int = 20,
                                 n_collect: int = None, *args, **kwargs) -> Iterable:
        """
        Shortcut for using run_until_no_stop for multi-page scraping.
        """
        if offset < 0:
            raise ValueError('Offset must be greater than or equal to zero.')

        elif n_collect and n_collect < 1:
            raise ValueError('n_collect must be greater than or equal to one.')

        def synthesizer():
            start_page = offset // results_per_page + 1

            while True:
                yield [{'url': direct_url, 'params': {'page': start_page}}, 'get']
                start_page += 1

        n_results = n_collect // results_per_page + int(n_collect % results_per_page != 0) if n_collect else None

        data = await self.run_until_no_stop(request_synthesizer=synthesizer(),
                                            not_stop_until=lambda result: result != [],
                                            n_results=n_results,
                                            *args, **kwargs)

        records = [record for page in data for record in page]
        adjusted_start = offset % results_per_page

        if n_collect:
            return records[adjusted_start:adjusted_start + n_collect]

        return records[adjusted_start:]

    def __del__(self):
        asyncio.run(
            self.session.close()
        )
