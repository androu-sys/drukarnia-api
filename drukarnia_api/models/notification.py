from typing import TypeVar
from drukarnia_api.models.base import BaseModel
from datetime import datetime
from attrs import frozen, field
from enum import IntEnum


C = TypeVar("C")


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
class NotificationModel(BaseModel):
    _id: str
    owner: str
    type: NotificationType | int = field(
        converter=NotificationType.new_with_other_fallback
    )
    seen: bool
    isLiked: bool
    createdAt: datetime = field(
        converter=datetime.fromisoformat,
    )
    details: dict
    __v: int
