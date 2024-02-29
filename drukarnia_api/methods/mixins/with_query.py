from attr import frozen, field, validators


@frozen
class MixinWithQuery:
    query: str = field(validator=validators.instance_of(str))
