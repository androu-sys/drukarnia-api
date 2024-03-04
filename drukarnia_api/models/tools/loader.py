from __future__ import annotations

from typing import Any, Iterable, TypeVar, overload

from drukarnia_api.models.tools.base import BaseModel
from drukarnia_api.models.tools.utils import normalize_dict_keys

_Model = TypeVar("_Model", bound=BaseModel)
SerializedModel = dict[str, Any]
SerializedData = SerializedModel | Iterable[SerializedModel]


@overload
def from_json(cls: type[_Model], data: SerializedModel) -> _Model:
    ...


@overload
def from_json(cls: type[_Model], data: Iterable[SerializedModel]) -> Iterable[_Model]:
    ...


def from_json(
        cls: type[_Model],
        data: SerializedData,
) -> _Model | Iterable[_Model]:
    if isinstance(data, dict):
        return cls(**normalize_dict_keys(data))

    if isinstance(data, Iterable):
        return (from_json(cls, record) for record in data)      # type: ignore[arg-type]

    msg = f"`from_json` got unexpected data type: {type(data)}. Expected `dict` or `list`"
    raise ValueError(msg)
