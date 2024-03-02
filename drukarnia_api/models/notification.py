from typing import TypeVar, Optional, Any
from drukarnia_api.models.tools import BaseModel, ModelRegistry
from datetime import datetime
from attrs import frozen, field, converters
from enum import IntEnum


C = TypeVar("C", bound="NotificationType")


class NotificationType(IntEnum):
    NEW_SUBSCRIBER: int = 300
    ADMIN_MSG: int = 10000

    @classmethod
    def new_with_other_fallback(cls: type[C], value: int) -> C | int:
        try:
            return NotificationType(value)
        except KeyError:
            return value


@frozen
class NotificationModel(BaseModel, metaclass=ModelRegistry):
    id_: str
    owner: Optional[str] = None
    type: Optional[NotificationType | int] = field(
        converter=converters.optional(NotificationType.new_with_other_fallback),
        default=None,
    )
    seen: Optional[bool] = field(
        converter=converters.optional(bool),
        default=None,
    )
    is_liked: Optional[bool] = field(
        converter=converters.optional(bool),
        default=None,
    )
    created_at: Optional[datetime] = field(
        converter=converters.optional(datetime.fromisoformat),
        default=None,
    )
    details: Optional[dict[str, Any]] = None
    v__: Optional[int] = None
