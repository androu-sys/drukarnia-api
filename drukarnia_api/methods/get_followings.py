from dataclasses import dataclass, field

from drukarnia_api.methods.get_followers import GetFollowers
from drukarnia_api.network.endpoints import DrukarniaEndpoints


@dataclass(kw_only=True)
class GetFollowings(
    GetFollowers,
):
    url: str = field(
        init=False,
        default=DrukarniaEndpoints.GetFollowings,
    )
