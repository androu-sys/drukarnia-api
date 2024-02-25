from typing import TypeVar, Type, overload, Generator
from abc import ABC, abstractmethod
DTO = TypeVar("DTO", bound="BaseDTO")


class BaseDTO(ABC):
    __slots__ = ()

    @abstractmethod
    def to_json(self) -> dict:
        raise NotImplementedError


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

        raise ValueError(f"`from_json` got unexpected data type: {type(data)}. Expected `dict` or `list`")
