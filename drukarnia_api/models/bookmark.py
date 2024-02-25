from drukarnia_api.models.base import BaseModel
from attrs import frozen, field
from drukarnia_api.models.article.bookmark_preview import BookmarkArticlePreviewModel
from datetime import datetime


def _extract_articles(data: list | dict) -> list[dict] | dict:
    if isinstance(data, dict):
        return data["article"]

    elif isinstance(data, list):
        return [_extract_articles(record) for record in data]

    raise TypeError(f"Expected list or dict got: `{type(data)}`")


@frozen
class BookmarkModel(BaseModel):
    _id: str
    name: str
    articlesNum: int
    owner: str
    createdAt: datetime = field(
        converter=datetime.fromisoformat,
    )
    updatedAt: datetime = field(
        converter=datetime.fromisoformat,
    )
    __v: int
    isLiked: bool = field(
        converter=bool
    )
    articles: list[BookmarkArticlePreviewModel] = field(
        converter=lambda data: BookmarkArticlePreviewModel.from_json(_extract_articles(data))
    )
