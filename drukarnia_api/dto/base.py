from abc import ABC
from typing import Type, TypeVar, overload
from attrs import define, asdict

DTO = TypeVar("DTO", bound="BaseDTO")


@define
class BaseDTO(ABC):
    __slots__ = ()

    def to_json(self) -> dict:
        return asdict(self)     # type: ignore

    @classmethod
    @overload
    def from_json(cls: Type[DTO], data: dict) -> DTO:
        ...

    @classmethod
    @overload
    def from_json(cls: Type[DTO], data: list) -> list[DTO]:
        ...

    @classmethod
    def from_json(cls: Type[DTO], data: list | dict) -> DTO | list[DTO]:
        if isinstance(data, dict):
            return cls(**data)

        elif isinstance(data, list):
            return [cls(**record) for record in data]

        raise ValueError(
            f"`from_json` got unexpected data type: {type(data)}. Expected `dict` or `list`"
        )
