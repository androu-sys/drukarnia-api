from attr import field, frozen, validators


@frozen(slots=False)
class MixinWithCurrentPassword:
    current_password: str = field(validator=validators.instance_of(str))
