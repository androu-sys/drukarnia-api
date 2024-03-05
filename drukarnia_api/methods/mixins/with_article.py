from attr import field, frozen, validators


@frozen(slots=False)
class MixinWithArticleId:
    article_id: str = field(
        validator=(
            validators.instance_of(str),
            validators.min_len(1),
        )
    )


@frozen(slots=False)
class MixinWithArticleSlug:
    article_slug: str = field(
        validator=(
            validators.instance_of(str),
            validators.min_len(1),
        )
    )
