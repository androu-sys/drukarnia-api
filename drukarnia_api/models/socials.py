from typing import Optional
from drukarnia_api.models.base import BaseModel
from attrs import frozen


@frozen
class SocialsModel(BaseModel):
    telegram: Optional[str]
    website: Optional[str]
