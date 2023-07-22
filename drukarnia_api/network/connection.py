import asyncio
from aiohttp import ClientSession
from typing import Any, Callable, Dict, Generator, Tuple, List, Iterable

from drukarnia_api.network.utils import to_json, _from_response
from drukarnia_api.network.cookie import DrukarniaCookies
from drukarnia_api.network.headers import Headers


class Connection:
    base_url = 'https://drukarnia.com.ua'

    def __init__(self, headers: Headers = None, cookie_jar: DrukarniaCookies = None, session: ClientSession = None):
        """
        Initialize a Connection object.

        Parameters:
            headers (Headers, optional): Headers to be used for the requests. Defaults to None.
            cookie_jar (DrukarniaCookies, optional): Cookie jar to be used for the requests. Defaults to None.
            session (ClientSession, optional): Custom aiohttp ClientSession to be used for the requests.
            Defaults to None.
        """
        self.cookieJar = cookie_jar if cookie_jar else DrukarniaCookies()
        self.headers = headers if headers else Headers()

        self.session = session
        self.custom_session = session is not None

    def __call__(self, session: ClientSession = None, *args, **kwargs) -> 'Connection':
        """
        Create or reuse an aiohttp ClientSession for making requests.

        Parameters:
            session (ClientSession, optional): Custom aiohttp ClientSession to be used for the requests.
            Defaults to None.

        Returns:
            Connection: The Connection instance with the specified session or the existing session.
        """
        if session:
            self.session = session
            return self

        elif self.session:
            return self

        self.session = ClientSession(
            base_url=self.base_url,
            cookie_jar=self.cookieJar,
            *args, **kwargs
        )

        return self

    async def __aenter__(self):
        """
        Context manager entry method for the Connection.

        Returns:
            Connection: The Connection instance.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit method for the Connection.

        Parameters:
            exc_type: Exception type.
            exc_val: Exception value.
            exc_tb: Exception traceback.
        """
        if self.custom_session is False:
            await self.session.close()

    async def request(self, method: str, url: str, output: str or list = None, **kwargs) -> Any:
        """
        Perform an HTTP request using the aiohttp ClientSession.

        Parameters:
            method (str): HTTP method for the request (e.g., 'GET', 'POST', 'PUT', 'PATCH', 'DELETE').
            url (str): The URL to which the request will be sent.
            output (str or list, optional): Expected output format, either 'json' or a list of fields. Defaults to None.
            **kwargs: Additional keyword arguments to be passed to aiohttp session.request.

        Returns:
            Any: The result of the HTTP request, parsed based on the provided output format.
        """
        if method in ['post', 'put', 'patch']:
            kwargs['data'] = await to_json(kwargs.get('data', {}))

        async with self.session.request(method.upper(), url, headers=self.headers.static, **kwargs) as response:
            return await _from_response(response, output)

    async def request_pool(self, heuristics: Iterable[Dict[str, Any]]) -> Tuple:
        """
        Perform a pool of HTTP requests using the given heuristics.

        Parameters:
            heuristics (Iterable[Dict[str, Any]]): An iterable of request heuristics (method, url, output, **kwargs).

        Returns:
            Tuple: A tuple containing the results of all the HTTP requests made in the pool.
        """

        # Create tasks
        tasks = [self.request(**kwargs) for kwargs in heuristics]

        # Get results
        return await asyncio.gather(*tasks)

    async def run_until_no_stop(self, request_synthesizer: Generator[Dict or List[Dict, str], None, None],
                                not_stop_until: Callable[[Any], bool], n_results: int = None,
                                batch_size: int = 5) -> List[Any]:
        """
        Run HTTP requests until a stopping condition is met.

        Parameters:
            request_synthesizer (Generator[Dict or List[Dict, str], None, None]):
                A generator that synthesizes request heuristics (method, url, output, **kwargs).
            not_stop_until (Callable[[Any], bool]):
                A callable that takes a response and returns True if the requests should continue, False otherwise.
            n_results (int, optional): The maximum number of results to fetch. Defaults to None (no limit).
            batch_size (int, optional): The number of requests to send in each batch. Defaults to 5.

        Returns:
            List[Any]: A list containing the results of the HTTP requests that meet the stopping condition.
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
