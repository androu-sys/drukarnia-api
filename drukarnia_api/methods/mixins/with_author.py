from attr import field, frozen, validators


@frozen(slots=False)
class MixinWithAuthorId:
    author_id: str = field(
        validator=(
            validators.instance_of(str),
            validators.min_len(1),
        )
    )


@frozen(slots=False)
class MixinWithUsername:
    username: str = field(
        validator=(
            validators.instance_of(str),
            validators.min_len(1),
        )
    )
