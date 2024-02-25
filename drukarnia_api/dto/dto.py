from typing import TypeVar, Type, overload, Generator

DTO = TypeVar("DTO", bound="BaseDTO")


class BaseDTO:
    __slots__ = ()

    @classmethod
    @overload
    def from_json(cls: Type[DTO], data: dict) -> DTO:
        ...

    @classmethod
    @overload
    def from_json(cls: Type[DTO], data: list) -> Generator[DTO, None, None]:
        ...

    @classmethod
    def from_json(cls: Type[DTO], data: list | dict) -> DTO | Generator[DTO, None, None]:
        if isinstance(data, dict):
            return cls(**data)

        elif isinstance(data, list):
            return (cls(**record) for record in data)

        raise ValueError(f"`from_json` got unexpected data type: {type(data)}. Expected `dict` or `list`")
