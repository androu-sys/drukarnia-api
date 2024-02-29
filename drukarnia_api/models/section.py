from typing import Optional, Union, TYPE_CHECKING
from datetime import datetime
from attrs import frozen, field, converters
from drukarnia_api.models.tools import BaseModel, Join, ModelRegistry

if TYPE_CHECKING:
    from drukarnia_api.models.article import ArticleModel


def _extract_article_dicts(data: list | dict) -> list[dict] | dict:
    if isinstance(data, dict):
        return data["article"]

    elif isinstance(data, list):
        return [_extract_article_dicts(record) for record in data]

    raise TypeError(f"Expected list or dict got: `{type(data)}`")


@frozen
class _BookmarkPreDescriptorModel(BaseModel):
    id_: str
    name: Optional[str] = None
    articlesNum: Optional[int] = None
    owner: Optional[str] = None
    createdAt: Optional[datetime] = field(
        converter=converters.optional(datetime.fromisoformat),
        default=None,
    )
    updatedAt: Optional[datetime] = field(
        converter=converters.optional(datetime.fromisoformat),
        default=None,
    )
    v__: Optional[int] = None
    isLiked: Optional[bool] = field(
        converter=converters.optional(bool),
        default=None,
    )
    articles: Optional[list[Union["ArticleModel", dict]]] = field(
        converter=converters.optional(_extract_article_dicts),
        default=None,
    )


class SectionModel(_BookmarkPreDescriptorModel, metaclass=ModelRegistry):
    articles: list["ArticleModel"] = Join("ArticleModel")
