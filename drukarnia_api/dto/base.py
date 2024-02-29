from abc import ABC
from typing import TypeVar
from attrs import define, asdict

DTO = TypeVar("DTO", bound="BaseDTO")


@define
class BaseDTO(ABC):
    __slots__ = ()

    def as_dict(self) -> dict:
        return asdict(self)
