from drukarnia_api.methods.get_followers import GetFollowers
from attrs import define, field


@define
class GetFollowings(GetFollowers):  # type: ignore[misc]
    url: str = field(
        init=False,
        default="/api/relationships/{author_id}/following",
    )
