from drukarnia_api.models.base import BaseModel
from attrs import frozen, field
from drukarnia_api.models.author.comment_owner import CommentAuthorModel
from datetime import datetime


@frozen
class CommentModel(BaseModel):
    _id: str
    comment: str
    owner: CommentAuthorModel = field(
        converter=CommentAuthorModel.from_json
    )
    article: str
    hiddenByAuthor: bool
    replyNum: int
    likesNum: int
    createdAt: datetime = field(
        converter=datetime.fromisoformat,
    )
    __v: int
    isLiked: bool = field(
        converter=bool
    )
    isBlocked: bool = field(
        converter=bool
    )
