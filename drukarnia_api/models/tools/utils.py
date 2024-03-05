import re
from typing import Any, TypeVar

D = TypeVar("D", bound=dict[str, Any])
Attr = TypeVar("Attr", bound=Any)


def _camel_to_snake(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def camel_to_snake_swap_underscores(name: str) -> str:
    non_private = name.lstrip("_")
    non_private_snake = _camel_to_snake(non_private)

    n_underscores = len(name) - len(non_private)
    return non_private_snake + "_" * n_underscores


def normalize_dict_keys(data: D) -> D:
    for key in list(data.keys()):
        data[camel_to_snake_swap_underscores(key)] = data.pop(key)

    return data
