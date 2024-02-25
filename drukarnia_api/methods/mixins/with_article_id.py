from attr import define, field, validators


@define
class MixinWithArticleID:
    article_id: str = field(validator=validators.instance_of(str))
