from typing import TypeVar, Type, Any
from drukarnia_api.models.tools.base import BaseModel


Self = TypeVar("Self", bound="ModelRegistry")


class ModelRegistry(type):
    _registry: dict[str, Type["BaseModel"]] = {}

    def __new__(cls: Type[Self], name: str, bases: tuple[Type["BaseModel"]], attrs: dict[str, Any]) -> Type["BaseModel"]:
        new_class = super().__new__(cls, name, bases, attrs)

        if not issubclass(new_class, BaseModel):
            raise TypeError(f"model `{name}` does not inherit from `BaseModel`.")

        cls._registry[name] = new_class
        return new_class

    @classmethod
    def get_model(cls: Type[Self], name: str) -> Type["BaseModel"]:
        if name in cls._registry:
            return cls._registry[name]

        raise KeyError(f"No model named '{name}' found")
