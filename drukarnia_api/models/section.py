from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, Self

from drukarnia_api.models.tools import BaseModel, Join, ModelRegistry, SerializedModel, from_json
from drukarnia_api.models.utils import optional_datetime_fromisoformat

if TYPE_CHECKING:
    from datetime import datetime

    from drukarnia_api.models.article import ArticleModel


def _custom_loader_with_hidden_data(
    instance: type[BaseModel],
    value: SerializedModel | str,
) -> BaseModel | Iterable[BaseModel]:
    if isinstance(value, dict):
        return from_json(instance, [value["article"]])

    if isinstance(value, list):
        return from_json(instance, (record["article"] for record in value))

    msg = f"Expected list or dict got: `{type(value)}`"
    raise TypeError(msg)


@dataclass(frozen=True, slots=True)
class SectionModel(BaseModel, metaclass=ModelRegistry):
    id_: str
    name: str | None = None
    articles_num: int | None = None
    owner: str | None = None
    created_at: datetime | str | None = None
    updated_at: datetime | str | None = None
    v__: int | None = None
    is_liked: bool | None = None

    articles: Join[
        Iterable[SerializedModel] | SerializedModel | None,
        Iterable[ArticleModel] | None,
    ] = Join("ArticleModel", _custom_loader_with_hidden_data)

    def __post_init__(self: Self) -> None:
        object.__setattr__(
            self,
            "created_at",
            optional_datetime_fromisoformat(self.created_at),
        )
        object.__setattr__(
            self,
            "updated_at",
            optional_datetime_fromisoformat(self.updated_at),
        )
