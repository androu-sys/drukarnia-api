from attr import frozen, field, validators


@frozen
class MixinWithArticleId:
    article_id: str = field(validator=validators.instance_of(str))
