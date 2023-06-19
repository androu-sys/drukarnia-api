from typing import Any, Callable
from warnings import warn
from datetime import datetime
from drukarnia_api.drukarnia_base.connection import Connection
from drukarnia_api.drukarnia_base.exceptions import DrukarniaElementDataError


class DrukarniaElement(Connection):
    """
    A class representing a printing element in a printing shop.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.all_collected_data = {}

    def _get_basetype_from_data(self, key: str, type_: Any = int, default: Any = 'auto'):
        """
        Get the value of the specified key from the author data dictionary and cast it to the specified type.

        Args:
            key (str): The key to access the value in the author data dictionary.
            type_ (Any): The type to cast the value to.
            default (Any): The default value if the key is not found. If set to 'auto', the default value will be
                           an instance of the specified type.

        Returns:
            Any: The value from the author data dictionary casted to the specified type or the default value.

        """
        if default == 'auto':
            default = type_()

        n = self._access_data(key, default)
        return type_(n) if n != default else n

    def _get_datetime_from_author_data(self, key: str):
        """
        Get a datetime object from the specified key in the author data dictionary.

        Args:
            key (str): The key to access the value in the author data dictionary.

        Returns:
            datetime: A datetime object parsed from the value in the author data dictionary.
        """
        date = self._access_data(key)

        if date:
            date = datetime.fromisoformat(date[:-1])

        return date

    def _update_data(self, new_data: dict):
        """
        Update the collected data with new data.

        Args:
            new_data (dict): The dictionary containing the new data to be added.
        """
        self.all_collected_data.update(new_data)

    def _access_data(self, key: str, default: Any = None):
        """
        Access a value from the collected data using the specified key.

        Args:
            key (str): The key to access the value in the collected data dictionary.
            default (Any): The default value to return if the key is not found.

        Returns:
            Any: The value from the collected data dictionary corresponding to the key, or the default value.
        """
        return self.all_collected_data.get(key, default)

    @staticmethod
    def _control_attr(attr: str, solution: str = 'call collect_data before') -> Callable:
        def decorator(func):
            async def wrapper(self_instance, *args, **kwargs):
                if getattr(self_instance, attr) is None:
                    raise DrukarniaElementDataError(attr, solution)

                return await func(self_instance, *args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def _is_authenticated(func):
        """
        Decorator to check if the headers contain a Cookie.

        Args:
            func (function): The function to decorate.

        Returns:
            function: The decorated function.
        """

        async def wrapper(self_instance, *args, **kwargs):
            """
            Wrapper function that performs the authentication check before calling the decorated function.

            Args:
                self_instance (DrukarniaElement): The instance of the DrukarniaElement class.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                Any: The result of the decorated function.
            """
            if 'Cookie' not in self_instance.session.headers:
                warn("Cookie data was not identified, it may cause an error for this request")

            return await func(self_instance, *args, **kwargs)

        return wrapper
