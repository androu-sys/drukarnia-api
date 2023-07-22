from aiohttp import ClientResponse
from typing import Any, Dict, List
from drukarnia_api.network.exceptions import DrukarniaAPIError

import json
import inspect


async def _from_response(response: ClientResponse, output: str or List[str] or None) -> Any:
    """
    Extracts data from the aiohttp ClientResponse based on the provided output.
    If the response status code is 400 or above, raises a DrukarniaAPIError.

    Parameters:
        response (ClientResponse): The aiohttp ClientResponse object.
        output (str or List[str] or None): A string, a list of strings, or None.
            If a string, it should be the attribute name to extract from the response.
            If a list of strings, it should be a list of attribute names to extract from the response.
            If None, returns an empty list.

    Returns:
        Any: The extracted data based on the provided output.
    """

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
    """
    Converts the provided data into a JSON string if it's a dictionary or a list.

    Parameters:
        data (Any): The data to be converted to JSON.

    Returns:
        Any: If the data is a dictionary or a list, it returns the JSON string representation.
            Otherwise, it returns the data unchanged.
    """

    if isinstance(data, Dict) or isinstance(data, List):
        return json.dumps(data)

    return data
