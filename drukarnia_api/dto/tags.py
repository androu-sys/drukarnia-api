from typing import Optional, Union

from attr import define, field, validators

from drukarnia_api.network.utils import _to_datetime
from datetime import datetime

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
    createdAt: Union[str, datetime] = field(
        validator=validators.instance_of(datetime),
        converter=_to_datetime,
    )
    default: bool = field(
        validator=validators.instance_of(bool),
    )
    mentionsNum: int = field(
        validator=(validators.instance_of(int), validators.ge(val=0)),
    )
