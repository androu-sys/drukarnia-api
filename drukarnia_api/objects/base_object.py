from datetime import datetime
from typing import Any, Callable, TypeVar, List, Awaitable
from functools import wraps
from attrdict import AttrDict
from drukarnia_api.network.connection import Connection


T = TypeVar('T')


def _synthesizer(offset, results_per_page, direct_url, kwargs):
    start_page = offset // results_per_page + 1

    while True:
        yield {'url': direct_url,
               'params': {'page': start_page},
               'output': 'json',
               'method': 'get'} | kwargs

        start_page += 1


def _to_datetime(date: str):
    if date:
        date = datetime.fromisoformat(date[:-1])

    return date


class DrukarniaElement(Connection):
    properties = AttrDict({})

    def _update_data(self, new_data: dict):
        self.properties.update(new_data)

    def _access_data(self, key: str, default: Any = None):
        return self.properties.get(key, default)

    async def multi_page_request(self, direct_url: str, offset: int = 0, results_per_page: int = 20,
                                 n_collect: int = None, key: str = None, **kwargs) -> List:

        assert offset >= 0, 'Offset must be greater than or equal to zero.'
        assert n_collect >= 1, 'n_collect must be greater than or equal to one.'

        n_results = (n_collect // results_per_page + int(n_collect % results_per_page != 0)) if n_collect else None

        data = await self.run_until_no_stop(
            request_synthesizer=_synthesizer(offset, results_per_page, direct_url, kwargs),
            not_stop_until=lambda result: result != [],
            n_results=n_results)

        if key is None:
            records = [record for page in data for record in page]

        else:
            records = [record for page in data for record in page.get(key, [])]

        adjusted_start = offset % results_per_page

        if n_collect:
            return records[adjusted_start:adjusted_start + n_collect]

        return records[adjusted_start:]

    @staticmethod
    def type_decorator(return_type: type) -> Callable[[Callable[..., T]], Callable[..., T]]:
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @wraps(func)
            async def wrapper(*args, **kwargs) -> T:
                result = await func(*args, **kwargs)

                if isinstance(return_type, datetime):
                    return _to_datetime(str(result))

                return return_type(result) if result is not None else None

            return wrapper

        return decorator

    @staticmethod
    def requires_attributes(attrs: List[str], solution: str = 'await collect_date() before.') -> Callable:
        def decorator(func: Callable[..., Awaitable]):
            @wraps(func)
            async def wrapper(self_instance, *args, **kwargs):
                if not all(getattr(self_instance, attr, None) for attr in attrs):
                    raise ValueError(f'Attributes {attrs} are required for this method. Possible solutions: {solution}')

                return await func(self_instance, *args, **kwargs)

            return wrapper

        return decorator
