import asyncio
import json

from aiohttp import ClientSession, ClientResponse
from typing import Any, Callable, Dict, Generator, Tuple, List, Iterable
import inspect
from drukarnia_api.drukarnia_base.exceptions import DrukarniaAPIError


async def _from_response(response: ClientResponse, output: str or List[str] or None) -> Any:

    if int(response.status) not in [200, 201]:
        data = await response.json()
        raise DrukarniaAPIError(data['message'], response.status,
                                response.request_info.method, str(response.request_info.url))

    if isinstance(output, str):
        data = await _from_response(response, [output])
        return data[0]

    if output is None:
        return []

    data = []
    for func_name in output:
        attr = getattr(response, func_name)

        if inspect.iscoroutinefunction(attr):
            data.append(await attr())

        elif callable(attr):
            data.append(attr())

        else:
            data.append(attr)

    return data


class Connection:
    base_url = 'https://drukarnia.com.ua'

    def __init__(self, session: ClientSession = None, headers: dict = None,
                 create_user_agent: bool = True, *args, **kwargs):

        # Save the aiohttp session
        if session:
            self.session = session
        else:
            headers_ = {'Content-Type': 'application/json'}
            if headers:
                headers_ = headers

            if create_user_agent:
                from fake_useragent import UserAgent

                headers_['User-Agent'] = UserAgent().random

            self.session = ClientSession(base_url=self.base_url, headers=headers_, *args, **kwargs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def _update_headers(self, new_data, inplace: bool = True) -> dict:
        if inplace:
            self.session.headers.update(new_data)

        return dict(self.session.headers) | new_data

    async def request(self, method: str, url: str, output: str or list = None, **kwargs) -> Any:

        if (method in ['post', 'put', 'patch']) and isinstance(kwargs.get('data', {}), dict):
            # if data parameter will be passed as None, (e.g. not passed at all)
            # aiohttp will switch to aplication/octet media type
            # which is not supported by Drukarnia API

            kwargs['data'] = json.dumps(kwargs.get('data', {}))

        async with self.session.request(method.upper(), url, **kwargs) as response:
            return await _from_response(response, output)

    async def request_pool(self, heuristics: Iterable[Dict[str, Any]]) -> Tuple:
        # Create tasks
        tasks = [self.request(**kwargs)
                 for kwargs in heuristics]

        # Get results
        return await asyncio.gather(*tasks)

    async def run_until_no_stop(self, request_synthesizer: Generator[Dict or List[Dict, str], None, None],
                                not_stop_until: Callable[[Any], bool], n_results: int = None,
                                batch_size: int = 5) -> List[Any]:
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
                                 n_collect: int = None, list_key: str or list = None, **kwargs) -> List:
        if offset < 0:
            raise ValueError('Offset must be greater than or equal to zero.')

        elif n_collect and n_collect < 1:
            raise ValueError('n_collect must be greater than or equal to one.')

        def synthesizer():
            start_page = offset // results_per_page + 1

            while True:
                yield {'url': direct_url,
                       'params': {'page': start_page},
                       'output': 'json',
                       'method': 'get'} | kwargs

                start_page += 1

        n_results = (n_collect // results_per_page + int(n_collect % results_per_page != 0)) if n_collect else None

        data = await self.run_until_no_stop(request_synthesizer=synthesizer(),
                                            not_stop_until=lambda result: result != [],
                                            n_results=n_results)

        adjusted_start = offset % results_per_page

        if isinstance(list_key, list):
            records = [[record for page in data for record in page.get(key, [])]
                       for key in list_key]

            if n_collect:
                return [record[adjusted_start:adjusted_start + n_collect] for record in records]

            return [record[adjusted_start:] for record in records]

        elif list_key is None:
            records = [record for page in data for record in page]

        else:
            records = [record for page in data for record in page.get(list_key, [])]

        if n_collect:
            return records[adjusted_start:adjusted_start + n_collect]

        return records[adjusted_start:]

    async def close_session(self):
        """
        Closes the aiohttp session.
        """
        await self.session.close()
