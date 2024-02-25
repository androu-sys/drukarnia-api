from typing import Optional, Union

from attr import define, field, validators

from drukarnia_api.network.utils import _to_datetime
from drukarnia_api.dto import AuthorRelationship
from datetime import datetime

@define
class Author:
    _id: str = field(
        validator=validators.instance_of(str),
    )
    name: str = field(
        validator=validators.instance_of(str),
    )
    avatar: Optional[str] = field(
        validator=validators.instance_of(str | type(None)),
    )
    username: str = field(validator=validators.instance_of(str))
    description: Optional[str] = field(
        validator=validators.instance_of(str | type(None))
    )
    followingNum: int = field(
        validator=(validators.instance_of(int), validators.ge(val=0))
    )
    followersNum: int = field(
        validator=validators.instance_of(int),
    )
    readNum: int = field(
        validator=(validators.instance_of(int), validators.ge(val=0)),
    )
    authorTags: list = field(
        validator=validators.instance_of(list),
    )
    createdAt: Union[str, datetime]  = field(
        validator=validators.instance_of(datetime),
        converter=_to_datetime,
    )
    relationships: AuthorRelationship = field(
        converter=lambda _dict: AuthorRelationship(**_dict),
    )
    articles: list = field(
        validator=validators.instance_of(list),
    )
