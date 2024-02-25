from drukarnia_api.methods.get_followers import GetFollowers
from attrs import frozen, field


@frozen
class GetFollowings(GetFollowers):  # type: ignore[misc]
    url: str = field(
        init=False,
        default="/api/relationships/{author_id}/following",
    )
