from typing import Optional, Union, TYPE_CHECKING
from attrs import frozen, field, converters
from drukarnia_api.models.tools import BaseModel, ModelRegistry, Join
from datetime import datetime

if TYPE_CHECKING:
    from drukarnia_api.models.article import ArticleModel


@frozen
class _PreDescriptorTagModel(BaseModel):
    id_: str
    name: Optional[str] = None
    slug: Optional[str] = None
    v__: Optional[int] = None
    createdAt: Optional[datetime] = field(
        converter=converters.optional(datetime.fromisoformat),
        default=None,
    )
    default: Optional[bool] = None
    mentionsNum: Optional[int] = None
    articles: Optional[Union[list["ArticleModel"], list[dict]]] = None


class TagModel(_PreDescriptorTagModel, metaclass=ModelRegistry):
    articles: list["ArticleModel"] = Join("ArticleModel")
