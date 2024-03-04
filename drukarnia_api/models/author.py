from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, Self

from drukarnia_api.models.tools import BaseModel, Join, ModelRegistry, SerializedModel
from drukarnia_api.models.utils import optional_datetime_fromisoformat

if TYPE_CHECKING:
    from datetime import datetime

    from drukarnia_api.models.article import ArticleModel
    from drukarnia_api.models.relationship import AuthorRelationshipsModel
    from drukarnia_api.models.socials import SocialsModel
    from drukarnia_api.models.tag import TagModel


@dataclass(frozen=True, slots=True)
class AuthorModel(BaseModel, metaclass=ModelRegistry):
    id_: str
    name: str | None = None
    avatar: str | None = None
    username: str | None = None
    description_short: str | None = None
    description: str | None = None
    following_num: int | None = None
    followers_num: int | None = None
    facebook_id: str | None = None
    google_id: str | None = None
    email: str | None = None
    read_num: int | None = None
    v__: int | None = None
    notifications_num: int | None = None
    created_at: datetime | str | None = None

    relationships: Join[
        SerializedModel | None,
        AuthorRelationshipsModel | None,
    ] = Join("AuthorRelationshipsModel")
    socials: Join[
        SerializedModel | None,
        SocialsModel | None,
    ] = Join("SocialsModel")
    author_tags: Join[
        Iterable[SerializedModel] | None,
        Iterable[TagModel] | None,
    ] = Join("TagModel")
    articles: Join[
        Iterable[SerializedModel] | None,
        Iterable[ArticleModel] | None,
    ] = Join("ArticleModel")

    def __post_init__(self: Self) -> None:
        object.__setattr__(
            self,
            "created_at",
            optional_datetime_fromisoformat(self.created_at),
        )
