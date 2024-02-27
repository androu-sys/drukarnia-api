from typing import Optional
from drukarnia_api.models.tools import BaseModel, ModelRegistry
from attrs import frozen


@frozen
class SocialsModel(BaseModel, metaclass=ModelRegistry):
    telegram: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    bluesky: Optional[str] = None
    facebook: Optional[str] = None
    linkedin: Optional[str] = None
    youtube: Optional[str] = None
    tiktok: Optional[str] = None
    website: Optional[str] = None
