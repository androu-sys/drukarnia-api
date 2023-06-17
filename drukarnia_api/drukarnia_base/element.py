from typing import Any
from warnings import warn
import inspect
from drukarnia_api.drukarnia_base.connection import Connection
from drukarnia_api.drukarnia_base.exceptions import DrukarniaElementDataError


class DrukarniaElement(Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.all_collected_data = {}

    def _control_attr(self, attr: str, solution: str = 'call collect_data before') -> None:
        """
        Check if the specified attribute exists and raise an error if it is None.
        """
        caller_name = inspect.currentframe().f_back.f_code.co_name

        if getattr(self, attr) is None:
            raise DrukarniaElementDataError(attr, caller_name, solution)

    def _get_basetype_from_author_data(self, key: str, type_: Any = int, default: Any = 'auto'):
        """
        Get the value of the specified key from the author data dictionary and cast it to the specified type.
        """

        if default == 'auto':
            default = type_()

        n = self._access_data(key, default)
        return type_(n) if n != default else n

    def _get_datetime_from_author_data(self, key: str):
        from datetime import datetime

        date = self._access_data(key)

        if date:
            date = datetime.fromisoformat(date[:-1])

        return date

    def _update_data(self, new_data: dict):
        self.all_collected_data.update(new_data)

    def _access_data(self, key: str, default: Any = None):
        return self.all_collected_data.get(key, default)

    @staticmethod
    def _is_authenticated(func):
        def wrapper(self_instance, *args, **kwargs):
            """
            Check if the headers contain a Cookie.
            """

            if 'Cookie' not in self_instance.session.headers:
                warn("Cookie data was not identified, it may cause an error for this request")

            return func(self_instance, *args, **kwargs)

        return wrapper
