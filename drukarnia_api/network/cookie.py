from aiohttp.cookiejar import CookieJar
import re
from typing import TYPE_CHECKING, Tuple, Dict, Any

if TYPE_CHECKING:
    from drukarnia_api.network.connection import Connection


async def _login(email: str, password: str, session: Connection) -> Tuple[str, Dict[str, Any]]:
    # Make a POST request to log in the author
    headers, info = await session.request(
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


class DrukarniaCookies(CookieJar):
    owner = None

    def __init__(self):
        super().__init__(unsafe=True)  # Set unsafe=True to allow third-party cookies.

    def login(self, email: str, password: str, session: Connection):
        cookie_str, self.owner = await _login(email, password, session)
        self.load(cookie_str)
