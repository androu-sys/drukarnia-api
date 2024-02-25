from typing import Optional
from attrs import frozen, field
from drukarnia_api.models.base import BaseModel
from drukarnia_api.models.socials import SocialsModel
from datetime import datetime


@frozen
class AuthorCardModel(BaseModel):
    _id: str
    name: str
    avatar: Optional[str]
    username: str
    descriptionShort: Optional[str]
    followingNum: int
    followersNum: int
    readNum: int
    createdAt: datetime = field(
        converter=datetime.fromisoformat,
    )
    socials: SocialsModel = field(
        converter=SocialsModel.from_json
    )
