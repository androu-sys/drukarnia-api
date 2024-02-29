from attr import frozen, field, validators


@frozen
class MixinWithTagId:
    tag_id: str = field(validator=validators.instance_of(str))


@frozen
class MixinWithTagSlug:
    tag_slug: str = field(validator=validators.instance_of(str))
