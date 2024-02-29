from attr import frozen, field, validators


@frozen
class MixinWithBookmarkId:
    bookmark_id: str = field(validator=validators.instance_of(str))
