from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from drukarnia_api.models.tools import BaseModel, Join, ModelRegistry, SerializedModel
from drukarnia_api.models.utils import optional_datetime_fromisoformat

if TYPE_CHECKING:
    from datetime import datetime

    from drukarnia_api.models.author import AuthorModel


@dataclass(frozen=True, slots=True)
class CommentModel(BaseModel, metaclass=ModelRegistry):
    id_: str
    comment: str
    article: str | None = None
    hidden_by_author: bool | None = None
    reply_num: int | None = None
    likes_num: int | None = None
    created_at: datetime | str | None = None
    is_liked: bool | None = None
    is_blocked: bool | None = None
    v__: int | None = None

    owner: Join[
        SerializedModel | None,
        AuthorModel | None,
    ] = Join("AuthorModel")

    def __post_init__(self: Self) -> None:
        object.__setattr__(
            self,
            "created_at",
            optional_datetime_fromisoformat(self.created_at),
        )
