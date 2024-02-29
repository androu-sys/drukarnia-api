from attr import frozen, field, validators


@frozen
class MixinWithAuthorId:
    author_id: str = field(validator=validators.instance_of(str))
