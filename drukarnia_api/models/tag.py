from typing import Optional, Union, Generator, TYPE_CHECKING
from attrs import frozen, field, converters
from drukarnia_api.models.tools import BaseModel, ModelRegistry, Join
from drukarnia_api.models.types import SerializedModel
from datetime import datetime

if TYPE_CHECKING:
    from drukarnia_api.models.article import ArticleModel


@frozen
class _PreDescriptorTagModel(BaseModel):
    id_: str
    name: Optional[str] = None
    slug: Optional[str] = None
    v__: Optional[int] = None
    created_at: Optional[datetime] = field(
        converter=converters.optional(datetime.fromisoformat),
        default=None,
    )
    default: Optional[bool] = None
    mentions_num: Optional[int] = None
    articles: Optional[Union[Generator["ArticleModel", None, None], list[SerializedModel]]] = None


class TagModel(_PreDescriptorTagModel, metaclass=ModelRegistry):
    articles: Generator["ArticleModel", None, None] = Join("ArticleModel")
