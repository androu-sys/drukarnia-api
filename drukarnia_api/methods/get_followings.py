from attrs import frozen, field
from drukarnia_api.methods.get_followers import GetFollowers
from drukarnia_api.network.endpoints import DrukarniaEndpoints


@frozen(kw_only=True)
class GetFollowings(
    GetFollowers,
):
    url = field(
        init=False,
        default=DrukarniaEndpoints.GetFollowings
    )
