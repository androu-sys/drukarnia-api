from typing import TypeVar, Any
from datetime import datetime


C = TypeVar("C", bound=Any)


def _to_datetime(date: str) -> datetime:
    """
    Convert a string representation of a date to a datetime object.

    Parameters:
        date (str): The date string in ISO format.

    Returns:
        datetime: The converted datetime object.
    """
    return datetime.fromisoformat(date[:-1])
