from typing import Optional, Union, TYPE_CHECKING
from datetime import datetime
from attrs import frozen, field, converters
from drukarnia_api.models.tools import BaseModel, Join, ModelRegistry

if TYPE_CHECKING:
    from drukarnia_api.models.author import AuthorModel


@frozen
class _CommentPreDescriptorModel(BaseModel):
    id_: str
    comment: Optional[str] = None
    article: Optional[str] = None
    hidden_by_author: Optional[bool] = None
    reply_num: Optional[int] = None
    likes_num: Optional[int] = None
    created_at: Optional[datetime] = field(
        converter=converters.optional(datetime.fromisoformat),
        default=None,
    )
    is_liked: Optional[bool] = field(
        converter=converters.optional(bool),
        default=None,
    )
    is_blocked: Optional[bool] = field(
        converter=converters.optional(bool),
        default=None,
    )
    v__: Optional[int] = None
    owner: Optional[Union["AuthorModel", dict]] = None


class CommentModel(_CommentPreDescriptorModel, metaclass=ModelRegistry):
    owner: "AuthorModel" = Join("AuthorModel")
