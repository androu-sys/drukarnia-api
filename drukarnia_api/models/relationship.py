from typing import Optional
from attrs import frozen
from drukarnia_api.models.tools import BaseModel, ModelRegistry


@frozen
class AuthorRelationshipsModel(BaseModel, metaclass=ModelRegistry):
    isSubscribed: Optional[bool] = None
    isBlocked: Optional[bool] = None
