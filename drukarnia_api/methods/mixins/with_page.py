from attr import define, field, validators


@define
class MixinWithPage:
    page_size: int = field(
        init=False,
        default=20,
    )

    # Default and unchangeable constant in current Drukarnia-API. Use it to standardize your code.
    page: int = field(
        default=1,
        validator=(
            validators.instance_of(int),
            validators.ge(0),
        ),
    )
