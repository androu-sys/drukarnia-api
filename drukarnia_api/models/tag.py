from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, Self

from drukarnia_api.models.tools import BaseModel, Join, ModelRegistry, SerializedModel
from drukarnia_api.models.utils import optional_datetime_fromisoformat

if TYPE_CHECKING:
    from datetime import datetime

    from drukarnia_api.models.article import ArticleModel
    from drukarnia_api.models.relationship import AuthorRelationshipsModel


@dataclass(frozen=True, slots=True)
class TagModel(BaseModel, metaclass=ModelRegistry):
    id_: str
    name: str | None = None
    slug: str | None = None
    v__: int | None = None
    created_at: datetime | str | None = None
    default: bool | None = None
    mentions_num: int | None = None

    articles: Join[
        Iterable[SerializedModel] | None,
        Iterable["ArticleModel"] | None,
    ] = Join("ArticleModel")
    relationships: Join[
        Iterable[SerializedModel] | None,
        "AuthorRelationshipsModel" | None
    ] = Join("AuthorRelationshipsModel")

    def __post_init__(self: Self) -> None:
        object.__setattr__(
            self,
            "created_at",
            optional_datetime_fromisoformat(self.created_at),
        )
