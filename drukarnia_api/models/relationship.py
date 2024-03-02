from typing import Optional
from attrs import frozen
from drukarnia_api.models.tools import BaseModel, ModelRegistry


@frozen
class AuthorRelationshipsModel(BaseModel, metaclass=ModelRegistry):
    is_subscribed: Optional[bool] = None
    is_blocked: Optional[bool] = None
