from attr import field, frozen, validators


@frozen(slots=False)
class MixinWithSectionId:
    section_id: str = field(validator=validators.instance_of(str))


@frozen(slots=False)
class MixinWithSectionName:
    section_name: str = field(validator=validators.instance_of(str))
