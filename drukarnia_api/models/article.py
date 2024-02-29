from typing import Optional, Union, TYPE_CHECKING
from datetime import datetime
from attrs import frozen, field, converters
from drukarnia_api.models.tools import BaseModel, Join, ModelRegistry
from drukarnia_api.models.relationship import AuthorRelationshipsModel

if TYPE_CHECKING:
    from drukarnia_api.models.tag import TagModel
    from drukarnia_api.models.author import AuthorModel
    from drukarnia_api.models.comment import CommentModel


@frozen
class _ArticlePreDescriptorModel(BaseModel):
    id_: str
    title: Optional[str] = None
    seoTitle: Optional[str] = None
    description: Optional[str] = None
    picture: Optional[str] = None
    thumbPicture: Optional[str] = None
    mainTag: Optional[str] = None
    mainTagSlug: Optional[str] = None
    mainTagId: Optional[str] = None
    ads: Optional[bool] = None
    index: Optional[bool] = None
    sensitive: Optional[bool] = None
    canonical: Optional[str] = None
    likeNum: Optional[int] = None
    commentNum: Optional[int] = None
    readTime: Optional[int] = None
    slug: Optional[str] = None
    content: Optional[dict] = None
    createdAt: Optional[datetime] = field(
        converter=converters.optional(datetime.fromisoformat),
        default=None,
    )
    isLiked: Optional[bool] = field(
        converter=converters.optional(bool),
        default=None,
    )
    isBookmarked: Optional[bool] = field(
        converter=converters.optional(bool),
        default=None,
    )
    relationships: Optional[AuthorRelationshipsModel] = field(
        converter=converters.optional(AuthorRelationshipsModel.from_json),
        default=None,
    )

    tags: Optional[list[Union["TagModel", dict]]] = None
    authorArticles: Optional[list[Union["ArticleModel", dict]]] = None
    owner: Optional[Union["AuthorModel", dict]] = field(
        converter=converters.optional(lambda data: {"id_": data} if isinstance(data, str) else data),
        default=None,
    )
    comments: Optional[list[Union["CommentModel", dict]]] = None
    recommendedArticles: Optional[list[Union["ArticleModel", dict]]] = None


class ArticleModel(_ArticlePreDescriptorModel, metaclass=ModelRegistry):
    tags: list["TagModel"] = Join("TagModel")
    authorArticles: list["ArticleModel"] = Join("ArticleModel")
    owner: "AuthorModel" = Join("AuthorModel")
    comments: list["CommentModel"] = Join("CommentModel")
    recommendedArticles: list["ArticleModel"] = Join("ArticleModel")
