from typing import TypeVar, Type, overload, Self, Optional, Generator, Any
from drukarnia_api.models.tools.base import BaseModel
from drukarnia_api.models.tools.registry import ModelRegistry
from typeguard import check_type, TypeCheckError


Model = TypeVar("Model", bound=BaseModel)
RType = Optional[Model | list[Model] | tuple[Model] | Generator[Model, None, None]]


class Join:
    _instance_field_name: str

    def __init__(self, model: str) -> None:
        self._model = model

    def __set_name__(self, owner, name):
        self._instance_field_name = name

    @overload
    def __get__(self: Self, instance: None, owner: Type[Model]) -> Self: ...
    @overload
    def __get__(self: Self, instance: Model, owner: Type[Model]) -> RType: ...

    def __get__(self: Self, instance: Model | None, owner: Type[Model]) -> RType:
        if instance is None:
            return self

        data = instance.__dict__.setdefault(self._instance_field_name, None)
        try:
            check_type(data, RType)
        except TypeCheckError:
            data = ModelRegistry.get_model(self._model).from_json(data)
            self.__set__(instance, data)

        return data

    def __set__(self, instance: Model, value: Any) -> None:
        instance.__dict__[self._instance_field_name] = value
