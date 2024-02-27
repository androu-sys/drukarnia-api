from drukarnia_api.models.tools.base import BaseModel


class ModelRegistry(type):
    _registry = {}

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)

        if not issubclass(new_class, BaseModel):
            raise TypeError(f"model `{name}` does not inherit from `BaseModel`.")

        cls._registry[name] = new_class
        return new_class

    @classmethod
    def __contains__(cls, name: str):
        return name in cls._registry

    @classmethod
    def get_model(cls, name: str) -> BaseModel:
        if name in cls._registry:
            return cls._registry[name]

        raise KeyError(f"No model named '{name}' found")
