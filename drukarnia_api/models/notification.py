from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, Any, Self, TypeVar

from drukarnia_api.models.tools import BaseModel, ModelRegistry
from drukarnia_api.models.utils import optional_datetime_fromisoformat

if TYPE_CHECKING:
    from datetime import datetime

C = TypeVar("C", bound="NotificationType")


class NotificationType(IntEnum):
    NEW_SUBSCRIBER: int = 300
    ADMIN_MSG: int = 10000

    @classmethod
    def new_with_other_fallback(cls: type[C], value: int) -> C | int:
        try:
            return cls(value)
        except KeyError:
            return value


@dataclass(frozen=True, slots=True)
class NotificationModel(BaseModel, metaclass=ModelRegistry):
    id_: str
    owner: str | None = None
    type_: NotificationType | int | None = None
    seen: bool | None = None
    is_liked: bool | None = None
    created_at: datetime | str | None = None
    details: dict[str, Any] | None = None
    v__: int | None = None

    def __post_init__(self: Self) -> None:
        object.__setattr__(
            self,
            "created_at",
            optional_datetime_fromisoformat(self.created_at),
        )
        if self.type_ is not None:
            object.__setattr__(
                self,
                "type_",
                NotificationType.new_with_other_fallback(self.type_),
            )
