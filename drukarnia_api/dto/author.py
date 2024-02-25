from typing import Optional
from attrs import define, field, validators
from drukarnia_api.dto.tag import Tag
from drukarnia_api.dto.base import BaseDTO
from drukarnia_api.dto.relationship import AuthorRelationship
from drukarnia_api.dto.socials import Socials
from drukarnia_api.dto.article import Article
from datetime import datetime


@define
class Author(BaseDTO):
    _id: str = field(
        validator=validators.instance_of(str),
    )
    name: str = field(
        validator=validators.instance_of(str),
    )
    avatar: Optional[str] = field(
        validator=validators.optional(validators.instance_of(str)),
    )
    username: str = field(
        validator=validators.instance_of(str),
    )
    descriptionShort: Optional[str] = field(
        validator=validators.optional(validators.instance_of(str)),
    )
    description: Optional[str] = field(
        validator=validators.optional(validators.instance_of(str)),
    )
    followingNum: int = field(
        validator=validators.instance_of(int),
    )
    followersNum: int = field(
        validator=validators.instance_of(int),
    )
    facebookId: Optional[str] = field(
        validator=validators.optional(validators.instance_of(str)),
    )
    googleId: Optional[str] = field(
        validator=validators.optional(validators.instance_of(str)),
    )
    email: str = field(
        validator=validators.instance_of(str),
    )
    readNum: int = field(
        validator=validators.instance_of(int),
    )
    authorTags: list[str] = field(
        converter=Tag.from_json
    )
    __v: int = field(
        validator=validators.instance_of(int),
    )
    notificationsNum: int = field(
        validator=validators.instance_of(int),
    )
    createdAt: datetime = field(
        validator=validators.instance_of(datetime),
        converter=lambda x: datetime.fromisoformat(x),
    )
    relationships: list[AuthorRelationship] = field(
        converter=AuthorRelationship.from_json
    )
    socials: Socials = field(
        converter=Socials.from_json
    )
    articles: list[Article] = field(
        converter=Article.from_json
    )
