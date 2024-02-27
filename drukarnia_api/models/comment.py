from typing import Optional, Union, TYPE_CHECKING
from datetime import datetime
from attrs import frozen, field, converters
from drukarnia_api.models.tools import BaseModel, ModelField, ModelRegistry

if TYPE_CHECKING:
    from drukarnia_api.models.author import AuthorModel


@frozen
class _CommentPreDescriptorModel(BaseModel):
    id_: str
    comment: Optional[str] = None
    article: Optional[str] = None
    hiddenByAuthor: Optional[bool] = None
    replyNum: Optional[int] = None
    likesNum: Optional[int] = None
    createdAt: Optional[datetime] = field(
        converter=converters.optional(datetime.fromisoformat),
        default=None,
    )
    isLiked: Optional[bool] = field(
        converter=converters.optional(bool),
        default=None,
    )
    isBlocked: Optional[bool] = field(
        converter=converters.optional(bool),
        default=None,
    )
    v__: Optional[int] = None
    owner: Optional[Union["AuthorModel", dict]] = None


class CommentModel(_CommentPreDescriptorModel, metaclass=ModelRegistry):
    owner: "AuthorModel" = ModelField("AuthorModel")
