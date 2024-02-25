from attr import define, field, validators


@define
class MixinWithTagID:
    tag_id: str = field(validator=validators.instance_of(str))
