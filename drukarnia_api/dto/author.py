from typing import Optional
from attr import define, field, validators, converters
from drukarnia_api.dto.utils import _to_datetime
from drukarnia_api.dto import AuthorRelationship
from drukarnia_api.dto.tag_summary import TagSummary
from datetime import datetime


@define
class Socials:
    name: str = field(
        validator=validators.instance_of(str),
    )
    url: str = field(
        validator=validators.instance_of(str),
    )


@define
class Author:
    _id: str = field(
        validator=validators.instance_of(str),
    )
    name: str = field(
        validator=validators.instance_of(str),
    )
    avatar: Optional[str] = field(
        validator=validators.instance_of(str | type(None)),
    )
    username: str = field(validator=validators.instance_of(str))
    description: Optional[str] = field(
        validator=validators.instance_of(str | type(None))
    )
    followingNum: int = field(
        validator=(validators.instance_of(int), validators.ge(val=0))
    )
    followersNum: int = field(
        validator=validators.instance_of(int),
    )
    readNum: int = field(
        validator=(validators.instance_of(int), validators.ge(val=0)),
    )
    authorTags: list[TagSummary] = field(
        converter=lambda data: [TagSummary(**tag) for tag in data]
    )
    socials: Socials = field(
        converter=lambda data: Socials(**data)
    )
    createdAt: datetime = field(
        validator=validators.instance_of(datetime),
        converter=_to_datetime,
    )
    relationships: AuthorRelationship = field(
        converter=lambda _dict: AuthorRelationship(**_dict),
    )
    articles: list = field(
        validator=validators.instance_of(list),
    )
