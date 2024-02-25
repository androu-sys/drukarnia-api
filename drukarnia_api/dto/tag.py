from typing import Optional

from attr import define, field, validators
from drukarnia_api.dto.base import BaseDTO
from datetime import datetime


@define
class Tag(BaseDTO):
    _id: str = field(
        validator=validators.instance_of(str),
    )
    name: str = field(
        validator=validators.instance_of(str),
    )
    slug: str = field(
        validator=validators.instance_of(str),
    )
    __v: Optional[int] = field(
        validator=validators.instance_of(int | type(None)),
    )
    createdAt: datetime = field(
        validator=validators.instance_of(datetime),
        converter=lambda x: datetime.fromisoformat(x),
    )
    default: bool = field(
        validator=validators.instance_of(bool),
    )
    mentionsNum: int = field(
        validator=(validators.instance_of(int), validators.ge(val=0)),
    )
