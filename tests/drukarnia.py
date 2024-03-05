import os
from typing import AsyncGenerator, Self

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from drukarnia_api import Drukarnia, models

load_dotenv()

TEST_EMAIL: str = os.getenv("TEST_EMAIL", default="")
TEST_PASSWORD: str = os.getenv("TEST_PASSWORD", default="")


# Validate environment variables
if (not TEST_EMAIL) or (not TEST_PASSWORD):
    msg = "Missing required environment variables: TEST_EMAIL or TEST_PASSWORD"
    raise OSError(msg)


@pytest.mark.asyncio()
class TestDrukarnia:
    @pytest_asyncio.fixture(name="api")
    async def drukarnia(self: Self) -> AsyncGenerator[Drukarnia, None]:
        async with Drukarnia() as api:
            yield api

    async def test_login(self: Self, api: "Drukarnia") -> None:
        author = await api.login(TEST_EMAIL, TEST_PASSWORD)
        assert isinstance(author, models.AuthorModel)
        assert author.email == TEST_EMAIL
