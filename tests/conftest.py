import pytest
from typing import AsyncGenerator
from drukarnia_api import Drukarnia


pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def api() -> AsyncGenerator[Drukarnia, None]:
    async with Drukarnia() as api:
        yield api
