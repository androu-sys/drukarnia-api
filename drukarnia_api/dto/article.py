from typing import Optional

from attr import define, field, validators
from drukarnia_api.dto import Tags


@define
class Article:
    _id: str = field(
        validator=validators.instance_of(str),
    )
    title: str = field(
        validator=validators.instance_of(str),
    )
    seoTitle: str = field(
        validator=validators.instance_of(str),
    )
    description: str = field(
        validator=validators.instance_of(str),
    )
    picture: Optional[str] = field(
        validator=validators.instance_of(str | type(None)),
    )
    mainTag: str = field(
        validator=validators.instance_of(str),
    )
    tags: Tags = field(
        converter=lambda _dict: Tags(**_dict),
    )
