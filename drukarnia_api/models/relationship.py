from attrs import frozen
from drukarnia_api.models.base import BaseModel


@frozen
class AuthorRelationshipModel(BaseModel):
    isSubscribed: bool
    isBlocked: bool
