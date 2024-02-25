from datetime import datetime
from typing import Optional
from attrs import frozen, field
from drukarnia_api.models.base import BaseModel


@frozen
class ArticleCardModel(BaseModel):
    _id: str
    title: str
    description: str
    mainTag: str
    mainTagId: str
    mainTagSlug: str
    tags: list[str]
    sensetive: bool
    canonical: Optional[str]
    likeNum: int
    commentNum: int
    readTime: int
    slug: str
    createdAt: datetime = field(
        converter=datetime.fromisoformat,
    )
    thumbPicture: Optional[str]
    owner: str
    isBookmarked: bool
