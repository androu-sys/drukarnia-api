import attrs
from typing import Any, Callable
from drukarnia_api.dto.base import BaseDTO


def starts_with(prefix: str) -> Callable[[Any, attrs.Attribute, str], None]:
    """
    Creates a custom validator function that checks if a string starts with the given prefix.

    Args:
        prefix (str): The prefix that the string should start with.

    Returns:
        Callable[[object, attr.Attribute, str], None]: A validator function to be used with attrs.
    """

    def validate(instance: Any, attribute: attrs.Attribute, value: str) -> None:
        """
        Validates whether the given value starts with the specified prefix.

        Args:
            instance (any): The instance that method is called on.
            attribute (attr.Attribute): The attribute being validated.
            value (str): The value of the attribute to validate.

        Raises:
            ValueError: If the value does not start with the specified prefix.
        """
        if not value.startswith(prefix):
            raise ValueError(f"{attribute.name} must start with '{prefix}'")

        if not isinstance(value, str):
            raise ValueError("value should be string")

    return validate


def to_dict(model: BaseDTO) -> dict:
    ...
