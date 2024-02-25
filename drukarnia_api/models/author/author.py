from typing import Optional
from attrs import frozen, field
from drukarnia_api.models.tag.summary import TagSummaryModel
from drukarnia_api.models.base import BaseModel
from drukarnia_api.models.relationship import AuthorRelationshipsModel
from drukarnia_api.models.socials import SocialsModel
from drukarnia_api.models.article.article_card import ArticleCardModel
from datetime import datetime


@frozen
class AuthorModel(BaseModel):
    _id: str
    name: str
    avatar: Optional[str]
    username: str
    descriptionShort: Optional[str]
    description: Optional[str]
    followingNum: int
    followersNum: int
    facebookId: Optional[str]
    googleId: Optional[str]
    email: Optional[str]
    readNum: int
    authorTags: list[TagSummaryModel] = field(
        converter=TagSummaryModel.from_json
    )
    __v: int
    notificationsNum: int
    createdAt: datetime = field(
        converter=datetime.fromisoformat,
    )
    relationships: list[AuthorRelationshipsModel] = field(
        converter=AuthorRelationshipsModel.from_json
    )
    socials: SocialsModel = field(
        converter=SocialsModel.from_json
    )
    articles: list[ArticleCardModel] = field(
        converter=ArticleCardModel.from_json
    )
