from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Iterable, Self

from drukarnia_api.models.tools import BaseModel, Join, ModelRegistry, SerializedModel, from_json
from drukarnia_api.models.utils import optional_datetime_fromisoformat

if TYPE_CHECKING:
    from datetime import datetime

    from drukarnia_api.models.author import AuthorModel
    from drukarnia_api.models.comment import CommentModel
    from drukarnia_api.models.relationship import AuthorRelationshipsModel
    from drukarnia_api.models.tag import TagModel


def _custom_loader_with_string_id(instance: type[BaseModel], value: SerializedModel | str) -> BaseModel:
    if isinstance(value, str):
        value = {"id_": value}

    return from_json(instance, value)


@dataclass(frozen=True, slots=True)
class ArticleModel(BaseModel, metaclass=ModelRegistry):
    id_: str
    title: str | None = None
    seo_title: str | None = None
    description: str | None = None
    picture: str | None = None
    thumb_picture: str | None = None
    main_tag: str | None = None
    main_tag_slug: str | None = None
    main_tag_id: str | None = None
    ads: bool | None = None
    index: bool | None = None
    sensitive: bool | None = None
    canonical: str | None = None
    like_num: int | None = None
    comment_num: int | None = None
    read_time: int | None = None
    slug: str | None = None
    content: dict[str, Any] | None = None
    created_at: datetime | str | None = None
    is_liked: bool | None = None
    is_bookmarked: bool | None = None

    relationships: Join[
        SerializedModel | None,
        AuthorRelationshipsModel | None,
    ] = Join("AuthorRelationshipsModel")
    tags: Join[
        Iterable[SerializedModel] | None,
        Iterable[TagModel] | None,
    ] = Join("TagModel")
    author_articles: Join[
        Iterable[SerializedModel] | None,
        Iterable[ArticleModel] | None,
    ] = Join("ArticleModel")
    owner: Join[
        SerializedModel | None,
        AuthorModel | None,
    ] = Join("AuthorModel", loader=_custom_loader_with_string_id)
    comments: Join[
        Iterable[SerializedModel] | None,
        Iterable[CommentModel] | None,
    ] = Join("CommentModel")
    recommended_articles: Join[
        Iterable[SerializedModel] | None,
        Iterable[ArticleModel] | None,
    ] = Join("ArticleModel")

    def __post_init__(self: Self) -> None:
        object.__setattr__(
            self,
            "created_at",
            optional_datetime_fromisoformat(self.created_at),
        )
