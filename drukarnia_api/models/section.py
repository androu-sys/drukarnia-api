from typing import Optional, Union, Generator, TYPE_CHECKING
from datetime import datetime
from attrs import frozen, field, converters
from drukarnia_api.models.tools import BaseModel, Join, ModelRegistry
from drukarnia_api.models.types import SerializedModel

if TYPE_CHECKING:
    from drukarnia_api.models.article import ArticleModel


def _extract_article_dicts(data: list[SerializedModel] | SerializedModel) -> list[SerializedModel] | SerializedModel:
    if isinstance(data, SerializedModel):
        return data["article"]      # type: ignore[no-any-return]

    elif isinstance(data, list):
        return [_extract_article_dicts(record) for record in data]

    raise TypeError(f"Expected list or dict got: `{type(data)}`")


@frozen
class _BookmarkPreDescriptorModel(BaseModel):
    id_: str
    name: Optional[str] = None
    articles_num: Optional[int] = None
    owner: Optional[str] = None
    created_at: Optional[datetime] = field(
        converter=converters.optional(datetime.fromisoformat),
        default=None,
    )
    updated_at: Optional[datetime] = field(
        converter=converters.optional(datetime.fromisoformat),
        default=None,
    )
    v__: Optional[int] = None
    is_liked: Optional[bool] = field(
        converter=converters.optional(bool),
        default=None,
    )
    articles: Optional[Generator[Union["ArticleModel", SerializedModel], None, None]] = field(
        converter=converters.optional(_extract_article_dicts),
        default=None,
    )


class SectionModel(_BookmarkPreDescriptorModel, metaclass=ModelRegistry):
    articles: Generator["ArticleModel", None, None] = Join("ArticleModel")
