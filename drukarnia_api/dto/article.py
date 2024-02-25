from datetime import datetime
from typing import Optional
from attr import define, field, validators
from drukarnia_api.dto.relationship import AuthorRelationship
from drukarnia_api.dto.tag import Tag
from drukarnia_api.dto.base import BaseDTO


@define
class Article(BaseDTO):
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
    tags: list[Tag] = field(
        converter=Tag.from_json,
    )
    ads: bool = field(
        validator=validators.instance_of(bool),
    )
    index: bool = field(
        validator=validators.instance_of(bool),
    )
    sensetive: bool = field(
        validator=validators.instance_of(bool),
    )
    canonical: Optional[str] = field(
        validator=validators.instance_of(str | type(None)),
    )
    likeNum: int = field(
        validator=(
            validators.instance_of(int),
            validators.ge(val=0),
        ),
    )
    commentNum: int = field(
        validator=(
            validators.instance_of(int),
            validators.ge(val=0),
        ),
    )
    readTime: int = field(
        validator=(
            validators.instance_of(int),
            validators.ge(val=0),
        ),
    )
    slug: str = field(
        validator=validators.instance_of(str),
    )
    mainTagSlug: str = field(
        validator=validators.instance_of(str),
    )
    mainId: str = field(
        validator=validators.instance_of(str),
    )
    createdAt: datetime = field(
        validator=validators.instance_of(datetime),
        converter=lambda x: datetime.fromisoformat(x),
    )
    thumbPicture: Optional[str] = field(
        validator=validators.instance_of(str | type(None)),
    )
    authorArticles = ...
    content = ...
    isLiked: int = field(
        validator=(
            validators.instance_of(int),
            validators.ge(val=0),
        ),
    )
    owner = ...
    isBookmarked: bool = field(
        validator=validators.instance_of(bool),
    )
    relationships: AuthorRelationship = field(
        converter=lambda _dict: AuthorRelationship(**_dict)
    )
    recommendedArticles = ...
    comments: list = field(
        validator=validators.instance_of(bool),
    )
