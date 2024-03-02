from typing import TypeVar, Type, overload
from drukarnia_api.models.tools.utils import normalize_dict_keys


Model = TypeVar("Model", bound="BaseModel")


class BaseModel:
    __slots__ = ()

    @classmethod
    @overload
    def from_json(cls: Type[Model], data: dict) -> Model:
        ...

    @classmethod
    @overload
    def from_json(cls: Type[Model], data: list) -> list[Model]:
        ...

    @classmethod
    def from_json(cls: Type[Model], data: list | dict) -> Model | list[Model]:
        if isinstance(data, dict):
            return cls(**normalize_dict_keys(data))

        elif isinstance(data, list):
            return [cls(cls.from_json(record)) for record in data]

        raise ValueError(f"`from_json` got unexpected data type: {type(data)}. Expected `dict` or `list`")
