from attrs import frozen
from drukarnia_api.models.base import BaseModel


@frozen
class TagSummaryModel(BaseModel):
    _id: str
    name: str
    slug: str
