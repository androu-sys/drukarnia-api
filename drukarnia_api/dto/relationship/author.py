from attr import define, field, validators


@define
class AuthorRelationship:
    isSubscribed: bool = field(
        validator=validators.instance_of(bool),
    )
    isBlocked: bool = field(
        validator=validators.instance_of(bool),
    )
