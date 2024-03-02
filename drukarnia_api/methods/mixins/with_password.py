from attr import frozen, field, validators


@frozen(slots=False)
class MixinWithCurrentPassword:
    current_password: str = field(validator=validators.instance_of(str))
