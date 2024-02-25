from datetime import datetime
from typing import Optional
from attrs import frozen, field
from drukarnia_api.models.base import BaseModel


@frozen
class ArticleFromAuthorModel(BaseModel):
    _id: str
    title: str
    description: str
    mainTag: str
    mainTagId: str
    mainTagSlug: str
    readTime: int
    slug: str
    createdAt: datetime = field(
        converter=datetime.fromisoformat,
    )
    picture: Optional[str]
    owner: str
    isBookmarked: bool
