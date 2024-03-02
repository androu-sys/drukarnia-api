from typing import TypeVar, Type, overload, Generator
from drukarnia_api.models.tools.utils import normalize_dict_keys
from drukarnia_api.models.types import SerializedModel


Model = TypeVar("Model", bound="BaseModel")


class BaseModel:
    __slots__ = ()

    @classmethod
    @overload
    def from_json(cls: Type[Model], data: SerializedModel) -> Model:
        ...

    @classmethod
    @overload
    def from_json(cls: Type[Model], data: list[SerializedModel]) -> Generator[Model, None, None]:
        ...

    @classmethod
    def from_json(
        cls: Type[Model],
        data: list[SerializedModel] | SerializedModel
    ) -> Model | Generator[Model, None, None]:
        if isinstance(data, dict):
            return cls(**normalize_dict_keys(data))

        elif isinstance(data, list):
            return (cls.from_json(record) for record in data)

        raise ValueError(f"`from_json` got unexpected data type: {type(data)}. Expected `dict` or `list`")
