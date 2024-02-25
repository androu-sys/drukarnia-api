from aiohttp import ClientResponse
from typing import NoReturn
from drukarnia_api.exceptions import DrukarniaAPIError


async def _check_response(response: ClientResponse) -> None | NoReturn:
    status = int(response.status)
    info = response.request_info

    if status in [200, 201]:
        return

    raise DrukarniaAPIError(
        message=(await response.json())["message"],
        status_code=status,
        request_type=info.method,
        request_url=str(info.url),
    )