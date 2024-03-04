from __future__ import annotations

from datetime import datetime


def optional_datetime_fromisoformat(value: str | datetime | None) -> datetime | None:
    if isinstance(value, datetime):
        return value
    if value is not None:
        return datetime.fromisoformat(value)
    return None
