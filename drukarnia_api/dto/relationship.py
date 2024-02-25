from attrs import define, field, validators
from drukarnia_api.dto.base import BaseDTO


@define
class AuthorRelationship(BaseDTO):
    isSubscribed: bool = field(
        validator=validators.instance_of(bool),
    )
    isBlocked: bool = field(
        validator=validators.instance_of(bool),
    )
