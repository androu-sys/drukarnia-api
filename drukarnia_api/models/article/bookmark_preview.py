from datetime import datetime
from attrs import frozen, field
from drukarnia_api.models.base import BaseModel
from drukarnia_api.models.author.bookmark_article import BookmarkArticleAuthorModel


@frozen
class BookmarkArticlePreviewModel(BaseModel):
    _id: str
    title: str
    readTime: int
    createdAt: datetime = field(
        converter=datetime.fromisoformat,
    )
    owner: BookmarkArticleAuthorModel = field(
        converter=BookmarkArticleAuthorModel.from_json
    )
