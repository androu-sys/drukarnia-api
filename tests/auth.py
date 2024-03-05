import os
from tests.conftest import *
import pytest
from dotenv import load_dotenv

from drukarnia_api import Drukarnia, models

load_dotenv()

TEST_EMAIL: str = os.getenv("TEST_EMAIL", default="")
TEST_PASSWORD: str = os.getenv("TEST_PASSWORD", default="")
TEST_USERNAME: str = os.getenv("TEST_USERNAME", default="")


# Validate environment variables
if (not TEST_EMAIL) or (not TEST_PASSWORD) or (not TEST_USERNAME):
    msg = "Missing required environment variables: TEST_EMAIL or TEST_PASSWORD or TEST_USERNAME"
    raise OSError(msg)


@pytest.mark.dependency(name="auth", scope="session")
async def test_login(api: "Drukarnia") -> None:
    author = await api.login(TEST_EMAIL, TEST_PASSWORD)
    assert isinstance(author, models.AuthorModel)
    assert author.email == TEST_EMAIL
