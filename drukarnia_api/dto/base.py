from __future__ import annotations

from abc import ABC
from typing import Any, Self, TypeVar

from attrs import asdict, define

DTO = TypeVar("DTO", bound="BaseDTO")


@define
class BaseDTO(ABC):
    __slots__ = ()

    def as_dict(self: Self) -> dict[str, Any]:
        return asdict(self)
