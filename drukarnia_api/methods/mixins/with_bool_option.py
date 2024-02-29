from attr import frozen, field, validators


@frozen
class MixinWithUnblockOption:
    unblock: bool = field(
        default=False,
        validator=validators.instance_of(bool),
    )


@frozen
class MixinWithUnsubscribeOption:
    unsubscribe: bool = field(
        default=False,
        validator=validators.instance_of(bool),
    )
