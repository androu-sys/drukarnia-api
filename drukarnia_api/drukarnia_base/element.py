from warnings import warn
import inspect
from drukarnia_api.drukarnia_base.connection import Connection
from drukarnia_api.drukarnia_base.exceptions import DrukarniaElementDataError


class DrukarniaElement(Connection):
    def __init__(self, username: str = None, _id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.author_data: dict = {'username': username, '_id': _id}

    async def is_authenticated(self) -> None:
        """
        Check if the headers contain a Cookie.
        """
        if 'Cookie' not in self.session.headers:
            warn("Cookie data was not identified, it may cause an error for this request")

    async def _control_attr(self, attr: str, solution: str = 'call collect_data before') -> None:
        """
        Check if the specified attribute exists and raise an error if it is None.
        """
        caller_name = inspect.currentframe().f_back.f_code.co_name

        if getattr(self, attr) is None:
            raise DrukarniaElementDataError(attr, caller_name, solution)

    def _get_basetype_from_author_data(self, key, type_='int'):
        """
        Get the value of the specified key from the author data dictionary and cast it to the specified type.
        """
        import builtins

        n = self.author_data.get(key, None)
        return getattr(builtins, type_)(n) if n else None

    def _get_str_from_author_data(self, key):
        """
        Get the value of the specified key from the author data dictionary and convert it to a string.
        """
        n = self.author_data.get(key, None)
        return str(n) if n else None
