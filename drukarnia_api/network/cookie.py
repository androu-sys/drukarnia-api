from aiohttp.cookiejar import SimpleCookie
from aiohttp import ClientSession
import re
from typing import TYPE_CHECKING, Tuple, Dict, Any

if TYPE_CHECKING:
    from drukarnia_api.network.connection import Connection


async def _login(email: str, password: str, connection: 'Connection') -> Tuple[str, Dict[str, Any]]:
    """
    Logs in the user by making a POST request to the login endpoint.

    Parameters:
        email (str): The email address of the user.
        password (str): The password of the user.
        connection ('Connection'): An instance of the 'Connection' class used to make HTTP requests.

    Returns:
        Tuple[str, Dict[str, Any]]: A tuple containing two values:
            - str: A string representing the cookies obtained after successful login.
            - Dict[str, Any]: A dictionary containing the response JSON data from the login endpoint.
    """
    headers, info = await connection.request(
        'post',
        '/api/users/login',
        data={"password": password, "email": email},
        output=['headers', 'json']
    )

    headers = str(headers)
    token = re.search(r'refreshToken=(.*?);', headers).group(1)
    device_id = re.search(r'deviceId=(.*?);', headers).group(1)

    cookies = f'deviceId={device_id}; token={token};'

    return cookies, info


class DrukarniaCookies(SimpleCookie):
    def __init__(self, *args, **kwargs):
        """
        Initializes the DrukarniaCookies class, a subclass of CookieJar.

        The unsafe parameter is set to True to allow third-party cookies.
        """
        super().__init__(*args, **kwargs)

        self.owner = None
        self.__authenticated = False

    async def login(self, email: str, password: str, connection: 'Connection'):
        """
        Logs in the user and stores the cookies in the instance.

        Parameters:
            email (str): The email address of the user.
            password (str): The password of the user.
            connection ('Connection'): An instance of the 'Connection' class used to make HTTP requests.
        """

        cookie_str, self.owner = await _login(email, password, connection)
        self.load(cookie_str)

        self.__authenticated = True

    @property
    def authenticated(self) -> bool:
        return self.__authenticated

    @staticmethod
    def sync_from_aiohttp_session(session: ClientSession) -> 'DrukarniaCookies':
        return DrukarniaCookies(session.cookie_jar.filter_cookies('/'))
