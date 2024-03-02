from typing import TypeVar, Type, overload, Self, Optional, Generator, Any, Union
from drukarnia_api.models.tools.base import BaseModel
from drukarnia_api.models.tools.registry import ModelRegistry


Model = TypeVar("Model", bound=BaseModel)
RType = Optional[Union[Model, Generator[Model, None, None]]]


class Join:
    _instance_field_name: str

    def __init__(self: Self, model: str) -> None:
        self._model = model

    def __set_name__(self: Self, owner: Type[Model], name: str) -> None:
        self._instance_field_name = name

    @overload
    def __get__(self: Self, instance: None, owner: Type[Model]) -> Self: ...
    @overload
    def __get__(self: Self, instance: Model, owner: Type[Model]) -> RType[Any]: ...

    def __get__(self: Self, instance: Model | None, owner: Type[Model]) -> RType[Any]:
        if instance is None:
            return self

        data = instance.__dict__.setdefault(self._instance_field_name, None)

        if isinstance(data, (dict, list)):
            data = ModelRegistry.get_model(self._model).from_json(data)

        return data

    def __set__(self: Self, instance: Model, value: Any) -> None:
        instance.__dict__[self._instance_field_name] = value
