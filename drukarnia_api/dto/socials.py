from typing import Optional
from drukarnia_api.dto.base import BaseDTO
from drukarnia_api.dto.utils import _optional_str
from attr import define


@define
class Socials(BaseDTO):
    telegram: Optional[str] = _optional_str()
    website: str = _optional_str()
