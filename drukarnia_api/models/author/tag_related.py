from typing import Optional
from attrs import frozen, field
from drukarnia_api.models.base import BaseModel
from drukarnia_api.models.relationship import AuthorRelationshipsModel


@frozen
class TagRelatedAuthorsModel(BaseModel):
    _id: str
    name: str
    avatar: Optional[str]
    username: str
    descriptionShort: Optional[str]
    relationship: AuthorRelationshipsModel = field(
        converter=AuthorRelationshipsModel.from_json
    )
