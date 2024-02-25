from attr import define, field, validators


@define
class MixinWithCommentID:
    comment_id: str = field(validator=validators.instance_of(str))
