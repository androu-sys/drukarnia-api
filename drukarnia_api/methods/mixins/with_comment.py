from attr import frozen, field, validators


@frozen(slots=False)
class MixinWithCommentId:
    comment_id: str = field(validator=validators.instance_of(str))


@frozen(slots=False)
class MixinWithCommentText:
    comment_text: str = field(validator=validators.instance_of(str))
