from typing import Optional
from drukarnia_api.models.base import BaseModel
from attrs import frozen


@frozen
class SocialsModel(BaseModel):
    telegram: Optional[str]
    instagram: Optional[str]
    twitter: Optional[str]
    bluesky: Optional[str]
    facebook: Optional[str]
    linkedin: Optional[str]
    youtube: Optional[str]
    tiktok: Optional[str]
    website: Optional[str]
