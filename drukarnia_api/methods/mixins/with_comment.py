from attr import field, frozen, validators


@frozen(slots=False)
class MixinWithCommentId:
    comment_id: str = field(
        validator=(
            validators.instance_of(str),
            validators.min_len(1),
        )
    )


@frozen(slots=False)
class MixinWithCommentText:
    comment_text: str = field(
        validator=(
            validators.instance_of(str),
            validators.min_len(1),
        )
    )
