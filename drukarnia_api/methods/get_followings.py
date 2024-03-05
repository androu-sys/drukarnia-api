from attrs import field, frozen

from drukarnia_api.methods.get_followers import GetFollowers
from drukarnia_api.network.endpoints import DrukarniaEndpoints


@frozen(kw_only=True)
class GetFollowings(   # type: ignore[misc]
    GetFollowers,
):
    url: str = field(
        init=False,
        default=DrukarniaEndpoints.GetFollowings,
    )
