import os
from tests.conftest import *
import pytest
from dotenv import load_dotenv

from drukarnia_api import Drukarnia, models

load_dotenv()

EMAIL: str = os.getenv("EMAIL", default="")
PASSWORD: str = os.getenv("PASSWORD", default="")
USERNAME: str = os.getenv("USERNAME", default="")


# Validate environment variables
if (not EMAIL) or (not PASSWORD) or (not USERNAME):
    msg = "Missing required environment variables: EMAIL or PASSWORD or USERNAME"
    raise OSError(msg)


@pytest.mark.dependency(name="auth", scope="session")
async def login(api: "Drukarnia") -> None:
    author = await api.login(EMAIL, PASSWORD)
    assert isinstance(author, models.AuthorModel)
    assert author.email == EMAIL
