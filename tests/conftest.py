import pytest
from typing import AsyncGenerator
from drukarnia_api import Drukarnia, models
from datetime import datetime


pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(name="api", scope="session")
async def api() -> AsyncGenerator[Drukarnia, None]:
    async with Drukarnia() as api:
        yield api


@pytest.fixture(name="target_author", scope="session")
def target_author_data() -> models.AuthorModel:
    return models.AuthorModel(
        id_="643a9b2786518bfbf4937598",
        username="mortisaeterna",
        created_at=datetime.fromisoformat("2023-04-15T12:40:07.203Z"),
    )
