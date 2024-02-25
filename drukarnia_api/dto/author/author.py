from typing import Optional
from attr import define, field, validators
from drukarnia_api.dto.article.article_summary import ArticleSummary
from drukarnia_api.dto.base import BaseDTO
from drukarnia_api.dto.utils import _str_field, _optional_str_field
from drukarnia_api.dto.socials import Socials
from drukarnia_api.dto.tag.tag_summary import TagSummary
from datetime import datetime


@define
class Author(BaseDTO):
    _id: str = _str_field()
    name: str = _str_field()
    username: str = _str_field()
    avatar: Optional[str] = _optional_str_field()
    description: Optional[str] = _optional_str_field()
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
