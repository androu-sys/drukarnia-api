from attrs import frozen
from drukarnia_api.models.base import BaseModel


@frozen
class AuthorRelationshipsModel(BaseModel):
    isSubscribed: bool
    isBlocked: bool
