from typing import Self
from tests.auth import *
from drukarnia_api.models import AuthorModel
from drukarnia_api.methods import PAGE_SIZE


class TestDrukarniaMethods:
    async def test_get_tag(self: Self, api: Drukarnia) -> None:
        tag = await api.get_tag("ukraine")
        assert tag.id_ == "63d79cc14b15077ac0e85134"

    async def test_get_author(
        self: Self,
        api: Drukarnia,
        target_author: AuthorModel,
    ) -> None:
        author = await api.get_author(
            username=target_author.username,
        )

        assert author.id_ == target_author.id_
        assert author.created_at == target_author.created_at

    async def test_get_followers(
        self: Self,
        api: Drukarnia,
        target_author: AuthorModel,
    ) -> None:
        author = await api.get_author(username=target_author.username)
        followers = await api.get_followers(
            author_id=target_author.id_,
            page=author.followers_num // PAGE_SIZE + 1,
        )

        followers = list(followers)
        # First follower
        assert followers[-1].username == "vesna_pryjde"

    async def test_get_followings(
        self: Self,
        api: Drukarnia,
        target_author: AuthorModel,
    ) -> None:
        author = await api.get_author(username=target_author.username)
        followings = await api.get_followings(
            author_id=target_author.id_,
            page=author.following_num // PAGE_SIZE + 1,
        )

        followings = list(followings)
        # First Following
        assert followings[-1].username == "godgivenformula"
