from typing import Optional
from attrs import frozen, field, converters
from drukarnia_api.models.tools import BaseModel, ModelRegistry
from datetime import datetime


@frozen
class TagModel(BaseModel, metaclass=ModelRegistry):
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
