from dataclasses import dataclass
from typing import Optional

from drukarnia_api.models.tools import BaseModel, ModelRegistry


@dataclass(frozen=True, slots=True)
class AuthorRelationshipsModel(BaseModel, metaclass=ModelRegistry):
    is_subscribed: Optional[bool] = None
    is_blocked: Optional[bool] = None
