from typing import Optional
import datetime
from attr import validators, field, define


@define
class ArticleSummary:
    _id: str = field(
        validator=validators.instance_of(str),
    )
    title: str = field(
        validator=validators.instance_of(str),
    )
    description: str = field(
        validator=validators.instance_of(str),
    )
    owner: str = field(
        validator=validators.instance_of(str),
    )
    thumbPicture: Optional[str] = field(
        validator=validators.optional(validators.instance_of(str)),
    )
    mainTag: str = field(
        validator=validators.instance_of(str),
    )
    tags: list[str] = field(
        validator=validators.deep_iterable(
            member_validator=validators.instance_of(str),
            iterable_validator=validators.instance_of(list),
        ),
    )
    sensitive: bool = field(
        validator=validators.instance_of(bool),
    )
    canonical: Optional[str] = field(
        validator=validators.optional(validators.instance_of(str)),
    )
    likeNum: int = field(
        validator=validators.instance_of(int),
    )
    commentNum: int = field(
        validator=validators.instance_of(int),
    )
    readTime: int = field(
        validator=validators.instance_of(int),
    )
    slug: str = field(
        validator=validators.instance_of(str),
    )
    mainTagSlug: str = field(
        validator=validators.instance_of(str),
    )
    mainTagId: str = field(
        validator=validators.instance_of(str),
    )
    createdAt: datetime.datetime = field(
        validator=validators.instance_of(datetime.datetime),
        converter=lambda x: datetime.datetime.fromisoformat(x) if isinstance(x, str) else x,
    )
    isBookmarked: bool = field(
        validator=validators.instance_of(bool),
    )
