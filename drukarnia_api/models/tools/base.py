from typing import TypeVar, Type, overload

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
            return cls(**data)

        elif isinstance(data, list):
            return [cls(**record) for record in data]

        raise ValueError(f"`from_json` got unexpected data type: {type(data)}. Expected `dict` or `list`")
