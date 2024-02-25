from typing import TypeVar, Any, Callable
from attrs import field, validators
from functools import wraps


def _field_factory(**kwargs: Any) -> Callable[[], field]:
    @wraps(field)
    def factory() -> Any:
        return field(**kwargs)

    return factory


_str_field: field = _field_factory(
    validator=validators.instance_of(str)
)
_int_gtz_freezed_field: field = _field_factory(
    validator=validators.instance_of(str)
)

field(f)

_optional_str_field: field = _field_factory(
    validator=validators.optional(validators.instance_of(str))
)

