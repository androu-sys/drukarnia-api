from attr import frozen, field, validators


@frozen
class MixinWithCommentId:
    comment_id: str = field(validator=validators.instance_of(str))
