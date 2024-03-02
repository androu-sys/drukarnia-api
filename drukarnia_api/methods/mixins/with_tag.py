from attr import frozen, field, validators


@frozen(slots=False)
class MixinWithTagId:
    tag_id: str = field(validator=validators.instance_of(str))


@frozen(slots=False)
class MixinWithTagSlug:
    tag_slug: str = field(validator=validators.instance_of(str))
