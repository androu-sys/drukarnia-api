from typing import Optional

from attr import define, field, validators

from drukarnia_api.network.utils import _to_datetime


@define
class Tags:
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
    createdAt: str = field(
        validator=validators.instance_of(str),
        converter=_to_datetime,
    )
    default: bool = field(
        validator=validators.instance_of(bool),
    )
    mentionsNum: int = field(
        validator=(validators.instance_of(int), validators.ge(val=0)),
    )
