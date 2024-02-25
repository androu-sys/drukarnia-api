from typing import Optional
from attr import define, field, validators
from drukarnia_api.dto.relationships import AuthorRelationship
from drukarnia_api.dto.article.article_summary import ArticleSummary
from drukarnia_api.dto.socials import Socials
from drukarnia_api.dto.tag.tag_summary import TagSummary
from datetime import datetime


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
        converter=lambda x: datetime.fromisoformat(x) if isinstance(x, str) else x,
    )
    relationships: AuthorRelationship = field(
        converter=lambda _dict: AuthorRelationship(**_dict),
    )
    articles: list[ArticleSummary] = field(
        validator=validators.instance_of(list[ArticleSummary]),
        converter=lambda data: [ArticleSummary(**article) for article in articles]
    )
