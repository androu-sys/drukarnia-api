from warnings import warn
from drukarnia_api.connection.connection import Connection


class DrukarniaElement(Connection):
    def __init__(self, username: str = None, _id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.author_data: dict = {'username': username, '_id': _id}

    async def is_authenticated(self) -> None:
        """
        Check if the headers contains Cookie.
        """

        if 'Cookie' not in self.session.headers:
            warn("Cookie data was not indentify, it may cause an error for this request")

    async def _control_attr(self, attr: str) -> None:
        if getattr(self, attr) is None:
            raise ValueError(f'{attr} is required. Try calling collect_data method before, or provide '
                             f'necessary data during initialization')

    def _get_basetype_from_author_data(self, key, type_='int'):
        import builtins

        n = self.author_data.get(key, None)
        return getattr(builtins, type_)(n) if n else None

    def _get_str_from_author_data(self, key):
        n = self.author_data.get(key, None)
        return str(n) if n else None

