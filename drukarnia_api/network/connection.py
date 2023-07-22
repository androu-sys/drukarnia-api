import asyncio
from aiohttp import ClientSession
from typing import Any, Callable, Dict, Generator, Tuple, List, Iterable

from drukarnia_api.network.utils import to_json, _from_response
from drukarnia_api.network.cookie import DrukarniaCookies
from drukarnia_api.network.headers import Headers


class Connection:
    base_url = 'https://drukarnia.com.ua'
    cookieJar = DrukarniaCookies()
    session = None

    def __init__(self, dynamic_user_generation: bool = False, default_headers=None):
        if default_headers is None:
            default_headers = {}

        self.headers = Headers(
            dynamic_user_generation,
            **default_headers
        )

    def __call__(self, session: ClientSession = None, *args, **kwargs) -> 'Connection':
        if session:
            self.session = session
            return self

        self.session = ClientSession(
            base_url=self.base_url,
            cookie_jar=self.cookieJar,
            *args, **kwargs
        )

        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def request(self, method: str, url: str, output: str or list = None, **kwargs) -> Any:
        if method in ['post', 'put', 'patch']:
            kwargs['data'] = await to_json(kwargs.get('data', {}))

        async with self.session.request(method.upper(), url, headers=self.headers.static, **kwargs) as response:
            return await _from_response(response, output)

    async def request_pool(self, heuristics: Iterable[Dict[str, Any]]) -> Tuple:
        # Create tasks
        tasks = [self.request(**kwargs) for kwargs in heuristics]

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
