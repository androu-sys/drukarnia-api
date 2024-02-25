from typing import Optional, Union

from attr import define, field, validators

from drukarnia_api.dto.utils import _to_datetime
from datetime import datetime


@define
class TagSummary:
    _id: str = field(
        validator=validators.instance_of(str),
    )
    name: str = field(
        validator=validators.instance_of(str),
    )
    slug: str = field(
        validator=validators.instance_of(str),
    )
