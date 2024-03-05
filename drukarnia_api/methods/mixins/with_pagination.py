from attr import field, frozen, validators

PAGE_SIZE: int = 20


@frozen(slots=False)
class MixinWithPagination:
    page: int = field(
        default=1,
        validator=(
            validators.instance_of(int),
            validators.ge(1),
        ),
    )

    # Default and unchangeable constant in current Drukarnia-API. Use it to standardize your code.
    page_size: int = field(
        init=False,
        default=PAGE_SIZE,
    )
