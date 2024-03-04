import pytest
import pytest_asyncio
from drukarnia_api import Drukarnia, models
from dotenv import load_dotenv
import os

load_dotenv()

TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


# Validate environment variables
if not TEST_EMAIL or not TEST_PASSWORD:
    raise EnvironmentError("Missing required environment variables: TEST_EMAIL or TEST_PASSWORD")


@pytest.mark.asyncio
class TestDrukarnia:
    @pytest_asyncio.fixture(name="api")
    async def drukarnia(self):
        async with Drukarnia() as api:
            yield api

    async def test_login(self, api: "Drukarnia"):
        author = await api.login(TEST_EMAIL, TEST_PASSWORD)
        assert isinstance(author, models.AuthorModel)
        assert author.email == TEST_EMAIL
