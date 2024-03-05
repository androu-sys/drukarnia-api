from typing import Any


def getattr_throw_on_none(instance: Any, name: str) -> Any:
    if (value := getattr(instance, name)) is None:
        msg = f"`{name}` attribute of `{instance.__class__}` cannot be None."
        raise TypeError(msg)

    return value
