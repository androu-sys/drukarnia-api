from attr import frozen, field, validators


@frozen(slots=False)
class MixinWithQuery:
    query: str = field(validator=validators.instance_of(str))
