from typing import Self
from tests.auth import *


class TestDrukarniaMethods:
    @pytest.mark.dependency(depends=["auth"])
    async def test_get_tag(self: Self, api: Drukarnia) -> None:
        tag = await api.get_tag("ukraine")
        assert tag.id_ == "63d79cc14b15077ac0e85134"
