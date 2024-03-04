from __future__ import annotations

from abc import ABCMeta
from typing import Any, ClassVar, TypeVar

from drukarnia_api.models.tools.base import BaseModel

Self = TypeVar("Self", bound="ModelRegistry")


class ModelRegistry(ABCMeta):
    _registry: ClassVar[dict[str, type[BaseModel]]] = {}

    def __new__(
        cls: type[Self],
        name: str,
        bases: tuple[type[BaseModel]],
        attrs: dict[str, Any],
    ) -> type[BaseModel]:
        new_class = super().__new__(cls, name, bases, attrs)

        if not issubclass(new_class, BaseModel):
            msg = f"model `{name}` does not inherit from `BaseModel`."
            raise TypeError(msg)

        cls._registry[name] = new_class
        return new_class

    @classmethod
    def get_model(cls: type[Self], name: str) -> type[BaseModel]:
        if name in cls._registry:
            return cls._registry[name]

        msg = f"No model named '{name}' found"
        raise KeyError(msg)
