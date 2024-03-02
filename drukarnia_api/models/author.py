from typing import Optional, TYPE_CHECKING, Generator, Union
from attrs import frozen, field, converters
from drukarnia_api.models.types import SerializedModel
from drukarnia_api.models.tools import ModelRegistry, Join, BaseModel
from datetime import datetime

if TYPE_CHECKING:
    from drukarnia_api.models.tag import TagModel
    from drukarnia_api.models.article import ArticleModel
    from drukarnia_api.models.relationship import AuthorRelationshipsModel
    from drukarnia_api.models.socials import SocialsModel


@frozen
class _AuthorPreDescriptorModel(BaseModel):
    id_: str
    name: Optional[str] = None
    avatar: Optional[str] = None
    username: Optional[str] = None
    description_short: Optional[str] = None
    description: Optional[str] = None
    following_num: Optional[int] = None
    followers_num: Optional[int] = None
    facebook_id: Optional[str] = None
    google_id: Optional[str] = None
    email: Optional[str] = None
    read_num: Optional[int] = None
    v__: Optional[int] = None
    notifications_num: Optional[int] = None
    relationships: Optional[Union[SerializedModel, "AuthorRelationshipsModel"]] = None
    socials: Optional[Union[SerializedModel, "SocialsModel"]] = None
    created_at: Optional[datetime] = field(
        default=None,
        converter=converters.optional(datetime.fromisoformat),
    )

    author_tags: Generator[Union[SerializedModel, "TagModel"], None, None] = []
    articles: Generator[Union[SerializedModel, "ArticleModel"], None, None] = []


class AuthorModel(_AuthorPreDescriptorModel, metaclass=ModelRegistry):
    """
    This is a little hack to include Descriptors in `attrs` generated class, while keeping the original
    signature and properties like `frozen`.
    """
    socials: "SocialsModel" = Join("SocialsModel")
    relationships: "AuthorRelationshipsModel" = Join("AuthorRelationshipsModel")
    author_tags: Generator["TagModel", None, None] = Join("TagModel")
    articles: Generator["ArticleModel", None, None] = Join("ArticleModel")
