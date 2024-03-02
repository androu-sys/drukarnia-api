from typing import Optional, Union, Generator, Any, TYPE_CHECKING
from datetime import datetime
from attrs import frozen, field, converters
from drukarnia_api.models.tools import BaseModel, Join, ModelRegistry
from drukarnia_api.models.types import SerializedModel
from drukarnia_api.models.relationship import AuthorRelationshipsModel

if TYPE_CHECKING:
    from drukarnia_api.models.tag import TagModel
    from drukarnia_api.models.author import AuthorModel
    from drukarnia_api.models.comment import CommentModel


@frozen
class _ArticlePreDescriptorModel(BaseModel):    # type: ignore[no-untyped-def]
    id_: str
    title: Optional[str] = None
    seo_title: Optional[str] = None
    description: Optional[str] = None
    picture: Optional[str] = None
    thumb_picture: Optional[str] = None
    main_tag: Optional[str] = None
    main_tag_slug: Optional[str] = None
    main_tag_id: Optional[str] = None
    ads: Optional[bool] = None
    index: Optional[bool] = None
    sensitive: Optional[bool] = None
    canonical: Optional[str] = None
    like_num: Optional[int] = None
    comment_num: Optional[int] = None
    read_time: Optional[int] = None
    slug: Optional[str] = None
    content: Optional[dict[str, Any]] = None
    created_at: Optional[datetime] = field(
        converter=converters.optional(datetime.fromisoformat),
        default=None,
    )
    i_liked: Optional[bool] = field(
        converter=converters.optional(bool),
        default=None,
    )
    is_bookmarked: Optional[bool] = field(
        converter=converters.optional(bool),
        default=None,
    )
    relationships: Optional[AuthorRelationshipsModel] = field(
        converter=converters.optional(AuthorRelationshipsModel.from_json),
        default=None,
    )

    tags: Optional[Generator[Union["TagModel", SerializedModel], None, None]] = None
    author_articles: Optional[Generator[Union["ArticleModel", SerializedModel], None, None]] = None
    owner: Optional[Union["AuthorModel", SerializedModel]] = field(
        converter=converters.optional(lambda data: {"id_": data} if isinstance(data, str) else data),
        default=None,
    )
    comments: Optional[Generator[Union["CommentModel", SerializedModel], None, None]] = None
    recommended_articles: Optional[Generator[Union["ArticleModel", SerializedModel], None, None]] = None


class ArticleModel(_ArticlePreDescriptorModel, metaclass=ModelRegistry):
    tags: Generator["TagModel", None, None] = Join("TagModel")
    author_articles: Generator["ArticleModel", None, None] = Join("ArticleModel")
    owner: "AuthorModel" = Join("AuthorModel")
    comments: Generator["CommentModel", None, None] = Join("CommentModel")
    recommended_articles: Generator["ArticleModel", None, None] = Join("ArticleModel")
