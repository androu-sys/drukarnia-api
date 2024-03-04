from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generic, Self, TypeVar, overload

from drukarnia_api.models.tools.loader import from_json
from drukarnia_api.models.tools.registry import ModelRegistry

if TYPE_CHECKING:
    from drukarnia_api.models.tools.base import BaseModel


IType = TypeVar("IType")
RType = TypeVar("RType")


class Join(Generic[IType, RType]):
    __slots__ = (
        "_model",
        "_loader",
        "_touched",
        "_instance_field_name",
    )
    _instance_field_name: str

    def __init__(
        self: Self,
        model: str,
        loader: Callable[[type[BaseModel], Any], Any] = from_json,
    ) -> None:
        self._model = model
        self._loader = loader
        self._touched: bool = False

    def __set_name__(self: Self, owner: type[BaseModel], name: str) -> None:
        self._instance_field_name = "_" + name

    @overload
    def __get__(self: Self, instance: None, owner: type[BaseModel]) -> Self: ...
    @overload
    def __get__(self: Self, instance: BaseModel, owner: type[BaseModel]) -> RType: ...

    def __get__(self: Self, instance: BaseModel | None, owner: type[BaseModel]) -> Self | RType | None:
        if instance is None:
            return self

        data: IType | RType | None = instance.__dict__.setdefault(self._instance_field_name, None)

        if data is None:
            return None
        if self._touched is False:
            data = self._loader(ModelRegistry.get_model(self._model), data)
            self.__set__(instance, data)     # type: ignore[arg-type]
            self._touched = True

        return data     # type: ignore[return-value]

    def __set__(
        self: Self,
        instance: BaseModel,
        value: IType,
    ) -> None:
        object.__setattr__(
            instance,
            self._instance_field_name,
            value,
        )
