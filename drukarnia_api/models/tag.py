from typing import Optional
from attrs import frozen, field
from drukarnia_api.models.base import BaseModel
from datetime import datetime


@frozen
class TagModel(BaseModel):
    _id: str
    name: str
    slug: str
    __v: Optional[int]
    createdAt: datetime = field(
        converter=datetime.fromisoformat,
    )
    default: bool
    mentionsNum: int
