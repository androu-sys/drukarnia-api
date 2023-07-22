from aiohttp import ClientResponse
from typing import Any, Dict, List
from drukarnia_api.network.exceptions import DrukarniaAPIError

import json
import inspect


async def _from_response(response: ClientResponse, output: str or List[str] or None) -> Any:

    if int(response.status) >= 400:
        data = await response.json()
        raise DrukarniaAPIError(data['message'], response.status,
                                response.request_info.method, str(response.request_info.url))

    if isinstance(output, str):
        data = await _from_response(response, [output])
        return data[0]

    if output is None:
        return []

    data = []
    for func_name in output:
        attr = getattr(response, func_name)

        if inspect.iscoroutinefunction(attr):
            data.append(await attr())

        elif callable(attr):
            data.append(attr())

        else:
            data.append(attr)

    return data


async def to_json(data: Any):
    if isinstance(data, Dict) or isinstance(data, List):
        return json.dumps(data)

    return data
