from typing import Optional
from attrs import frozen
from drukarnia_api.models.base import BaseModel


@frozen
class BookmarkArticleAuthorModel(BaseModel):
    _id: str
    name: str
    avatar: Optional[str]
