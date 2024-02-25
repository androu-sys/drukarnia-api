from typing import Optional
from attrs import define, field, validators
from drukarnia_api.dto.base import BaseDTO
from drukarnia_api.dto.socials import SocialsDTO


@define
class UserInfoUpdate(BaseDTO):
    name: Optional[str] = field(
        default=None,
        validator=validators.optional(validators.instance_of(str))
    )
    description: Optional[str] = field(
        default=None,
        validator=validators.optional(validators.instance_of(str))
    )
    username: Optional[str] = field(
        default=None,
        validator=validators.optional(validators.instance_of(str))
    )
    description_short: Optional[str] = field(
        default=None,
        validator=validators.optional(validators.instance_of(str))
    )
    donate_url: Optional[str] = field(
        default=None,
        validator=validators.optional(validators.instance_of(str))
    )
    socials: SocialsDTO = field(
        factory=SocialsDTO,
        validator=validators.instance_of(SocialsDTO),
    )
