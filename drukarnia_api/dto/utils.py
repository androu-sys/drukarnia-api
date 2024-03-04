from typing import Any, Callable

import attrs


def starts_with(prefix: Any) -> Callable[[Any, attrs.Attribute, Any], None]:    # type: ignore[type-arg]
    """Create a custom validator function that checks if a string starts with the given prefix.

    Args:
    ----
        prefix (str): The prefix that the string should start with.

    Returns:
    -------
        Callable[[object, attr.Attribute, str], None]: A validator function to be used with attrs.

    """

    def validate(_: Any, attribute: attrs.Attribute, value: Any) -> None:    # type: ignore[type-arg]
        """Validate whether the given value starts with the specified prefix.

        Args:
        ----
            _ (any): The instance that method is called on.
            attribute (attr.Attribute): The attribute being validated.
            value (str): The value of the attribute to validate.

        Raises:
        ------
            ValueError: If the value does not start with the specified prefix.

        """
        if not isinstance(value, str):
            msg = f"Value must be of type {str}."
            raise TypeError(msg)

        if not value.startswith(prefix):
            msg = f"{attribute.name} must start with '{prefix}'"
            raise ValueError(msg)

    return validate
