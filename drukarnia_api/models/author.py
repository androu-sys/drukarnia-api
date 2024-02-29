from typing import Optional, TYPE_CHECKING, Union
from attrs import frozen, field, converters
from drukarnia_api.models.tools import ModelRegistry, Join, BaseModel
from drukarnia_api.models.relationship import AuthorRelationshipsModel
from drukarnia_api.models.socials import SocialsModel
from datetime import datetime

if TYPE_CHECKING:
    from drukarnia_api.models.tag import TagModel
    from drukarnia_api.models.article import ArticleModel


@frozen
class _AuthorPreDescriptorModel(BaseModel):
    id_: str
    name: Optional[str] = None
    avatar: Optional[str] = None
    username: Optional[str] = None
    descriptionShort: Optional[str] = None
    description: Optional[str] = None
    followingNum: Optional[int] = None
    followersNum: Optional[int] = None
    facebookId: Optional[str] = None
    googleId: Optional[str] = None
    email: Optional[str] = None
    readNum: Optional[int] = None
    v__: Optional[int] = None
    notificationsNum: Optional[int] = None
    relationships: Optional[AuthorRelationshipsModel] = field(
        converter=SocialsModel.from_json,
        factory=dict,
    )
    socials: Optional[SocialsModel] = field(
        converter=SocialsModel.from_json,
        factory=dict,
    )
    createdAt: Optional[datetime] = field(
        default=None,
        converter=converters.optional(datetime.fromisoformat),
    )

    authorTags: list[Union[dict, "TagModel"]] = []
    articles: list[Union[dict, "ArticleModel"]] = []


class AuthorModel(_AuthorPreDescriptorModel, metaclass=ModelRegistry):
    """
    This is a little hack to include Descriptors in `attrs` generated class, while keeping the original
    signature and properties like `frozen`.
    """
    authorTags: list["TagModel"] = Join("TagModel")
    articles: list["ArticleModel"] = Join("ArticleModel")
