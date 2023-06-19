import asyncio
from aiohttp import ClientSession, ClientResponse, ContentTypeError
from typing import Any, Callable, Dict, Generator, Tuple, List, Iterable
import inspect
from drukarnia_api.drukarnia_base.exceptions import DrukarniaAPIError
from warnings import warn


async def _from_response(response: ClientResponse, output: str or List[str]) -> Any:
    """
    Extracts data from the response object based on the specified output format.
    :param response: The response object.
    :param output: The specified output format.
    :return: Extracted data.
    """

    if response.status not in [200, 201]:
        data = await response.json()
        raise DrukarniaAPIError(data['message'], response.status,
                                response.request_info.method, str(response.request_info.url))

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
        :param session: The aiohttp session.
        :param headers: The headers for the HTTP requests.
        :param create_user_agent: Whether to create a random User-Agent header.
        """

        # Save the aiohttp session
        if session:
            self.session = session
        else:
            headers_ = {}
            if headers:
                headers_ = headers

            if create_user_agent:
                from fake_useragent import UserAgent

                headers_['User-Agent'] = UserAgent().random

            self.session = ClientSession(base_url=self.base_url, headers=headers_, *args, **kwargs)

    async def get(self, url: str, params: dict = None,
                  output: str or list = 'json', *args, **kwargs) -> dict or tuple:
        """
        Sends a GET request and returns the response data based on the specified output format.
        :param url: The URL for the GET request.
        :param params: The query parameters for the request.
        :param output: The specified output format.
        :return: The response data.
        """

        async with self.session.get(url, params=params, *args, **kwargs) as response:
            return await _from_response(response, output)

    async def put(self, url: str, params: dict = None,
                  output: str or list = 'json', *args, **kwargs) -> dict or tuple:
        """
        Sends a PUT request and returns the response data based on the specified output format.
        :param url: The URL for the PUT request.
        :param params: The query parameters for the request.
        :param output: The specified output format.
        :return: The response data.
        """
        async with self.session.put(url, params=params, *args, **kwargs) as response:
            return await _from_response(response, output)

    async def patch(self, url: str, data: dict = None,
                    output: str or list = 'json', **kwargs) -> dict or tuple:
        """
        Sends a PATCH request and returns the response data based on the specified output format.
        :param url: The URL for the PATCH request.
        :param data: The data for the request.
        :param output: The specified output format.
        :return: The response data.
        """
        async with self.session.patch(url, data=data, **kwargs) as response:
            return await _from_response(response, output)

    async def post(self, url: str, data: dict = None,
                   output: str or list = 'json', **kwargs) -> dict or tuple:
        """
        Sends a POST request and returns the response data based on the specified output format.
        :param url: The URL for the POST request.
        :param data: The data for the request.
        :param output: The specified output format.
        :return: The response data.
        """
        async with self.session.post(url, data=data, **kwargs) as response:
            return await _from_response(response, output)

    async def delete(self, url: str, output: str or list = 'read', **kwargs):
        """
        Sends a DELETE request and returns the response data based on the specified output format.
        :param url: The URL for the DELETE request.
        :param output: The specified output format.
        :return: The response data.
        """
        async with self.session.delete(url, **kwargs) as response:
            return await _from_response(response, output)

    async def request_pool(self, heuristics: Iterable[dict]) -> Tuple:
        """
        Sends multiple GET requests concurrently.
        :param heuristics: The list of dictionaries containing request information.
        :return: The responses from the requests.
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
        :param request_synthesizer: The generator that yields request information.
        :param not_stop_until: The function that determines the stopping condition.
        :param n_results: The maximum number of results to collect.
        :param batch_size: The number of requests to send in each batch.
        :return: The aggregated results.
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
                                 n_collect: int = None, list_key: str = None, *args, **kwargs) -> List:
        """
        Shortcut for using run_until_no_stop for multi-page scraping.
        :param list_key: key of main list results on each API page.
        :param direct_url: The URL for the requests.
        :param offset: The starting offset.
        :param results_per_page: The number of results per page.
        :param n_collect: The number of results to collect.
        :return: The collected results.
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

        n_results = (n_collect // results_per_page + int(n_collect % results_per_page != 0)) if n_collect else None

        data = await self.run_until_no_stop(request_synthesizer=synthesizer(),
                                            not_stop_until=lambda result: result != [],
                                            n_results=n_results,
                                            *args, **kwargs)

        if list_key is None:
            records = [record for page in data for record in page]

        else:
            records = [record for page in data for record in page.get(list_key, [])]

        adjusted_start = offset % results_per_page

        if n_collect:
            return records[adjusted_start:adjusted_start + n_collect]

        return records[adjusted_start:]

    async def close_session(self):
        """
        Closes the aiohttp session.
        """
        await self.session.close()
