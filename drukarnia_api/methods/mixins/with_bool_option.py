from attr import frozen, field, validators


@frozen(slots=False)
class MixinWithUnblockOption:
    unblock: bool = field(
        default=False,
        validator=validators.instance_of(bool),
    )


@frozen(slots=False)
class MixinWithRelationsOption:
    with_relations: bool = field(
        validator=validators.instance_of(bool),
        default=False,
    )


@frozen(slots=False)
class MixinWithUnbookmarkOption:
    unbookmark: bool = field(
        default=False,
        validator=validators.instance_of(bool),
    )


@frozen(slots=False)
class MixinWithUnsubscribeOption:
    unsubscribe: bool = field(
        default=False,
        validator=validators.instance_of(bool),
    )


@frozen(slots=False)
class MixinWithUnlikeOption:
    unlike: bool = field(
        default=False,
        validator=validators.instance_of(bool),
    )


@frozen(slots=False)
class MixinWithPreviewOption:
    preview: bool = field(
        default=False,
        validator=validators.instance_of(bool),
    )
