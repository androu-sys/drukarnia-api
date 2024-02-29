from attr import frozen, field, validators


@frozen
class MixinWithSectionId:
    section_id: str = field(validator=validators.instance_of(str))
