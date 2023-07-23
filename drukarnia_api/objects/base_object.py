from datetime import datetime
from typing import Any, Callable, TypeVar, List, Awaitable
from attrdict import AttrDict
from drukarnia_api.network.connection import Connection


T = TypeVar('T')


def _synthesizer(offset: int, results_per_page: int, direct_url: str, kwargs: dict):
    """
    Generates requests with pagination.

    Parameters:
        offset (int): The starting offset for pagination.
        results_per_page (int): The number of results per page.
        direct_url (str): The base URL for the requests.
        kwargs (dict): Additional keyword arguments for the requests.

    Yields:
        dict: A dictionary containing request parameters.
    """
    start_page = offset // results_per_page + 1

    while True:
        yield {'url': direct_url,
               'params': {'page': start_page},
               'output': 'json',
               'method': 'get'} | kwargs

        start_page += 1


def _to_datetime(date: str) -> datetime:
    """
    Convert a string representation of a date to a datetime object.

    Parameters:
        date (str): The date string in ISO format.

    Returns:
        datetime: The converted datetime object.
    """
    if date:
        date = datetime.fromisoformat(date[:-1])

    return date


class DrukarniaElement(Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = AttrDict({})

    def _update_data(self, new_data: dict):
        """
        Update the data properties of the DrukarniaElement.

        Parameters:
            new_data (dict): The new data to update the properties with.
        """
        self.data.update(new_data)

    def _access_data(self, key: str, default: Any = None) -> Any:
        """
        Access data from the properties of the DrukarniaElement.

        Parameters:
            key (str): The key to access the data.
            default (Any, optional): The default value to return if the key is not found. Defaults to None.

        Returns:
            Any: The value associated with the given key or the default value if the key is not found.
        """
        return self.data.get(key, default)

    async def multi_page_request(self, direct_url: str, offset: int = 0, results_per_page: int = 20,
                                 n_collect: int = None, key: str = None, **kwargs) -> List:
        """
        Perform a multi-page request with pagination.

        Parameters:
            direct_url (str): The base URL for the requests.
            offset (int, optional): The starting offset for pagination. Defaults to 0.
            results_per_page (int, optional): The number of results per page. Defaults to 20.
            n_collect (int, optional): The total number of results to collect. Defaults to None.
            key (str, optional): The key to extract records from the returned data. Defaults to None.
            **kwargs: Additional keyword arguments for the requests.

        Returns:
            List: A list of records extracted from the paginated data.
        """
        assert offset >= 0, 'Offset must be greater than or equal to zero.'
        assert (n_collect is None) or (n_collect >= 1), 'n_collect must be greater than or equal to one.'

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
        """
        A decorator to enforce the return type of a method.

        Parameters:
            return_type (type): The expected return type.

        Returns:
            Callable: The decorated method with enforced return type.
        """
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            async def wrapper(*args, **kwargs) -> T:
                result = await func(*args, **kwargs)
                if result is None: return

                if return_type is datetime:
                    return _to_datetime(str(result))

                return return_type(result)

            return wrapper

        return decorator

    @staticmethod
    def requires_attributes(attrs: List[str], solution: str = 'await collect_data() before.') -> Callable:
        """
        A decorator to ensure that certain attributes are present before executing a method.

        Parameters:
            attrs (List[str]): A list of attribute names that must be present.
            solution (str, optional): A suggestion for a possible solution. Defaults to 'await collect_date() before.'.

        Returns:
            Callable: The decorated method with attribute requirement checks.
        """
        def decorator(func: Callable[..., Awaitable]):
            async def wrapper(self_instance, *args, **kwargs):
                if any([(await getattr(self_instance, attr)) is None for attr in attrs]):
                    raise ValueError(f'This function requires attributes {attrs}, '
                                     f'which are missing. Possible solutions: {solution}')

                return await func(self_instance, *args, **kwargs)

            return wrapper

        return decorator
