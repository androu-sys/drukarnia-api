from datetime import datetime
from typing import Optional
from attr import define, field, validators
from drukarnia_api.dto import AuthorRelationship, Tags
from drukarnia_api.dto.utils import _to_datetime


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
        converter=_to_datetime,
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
