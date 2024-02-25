from datetime import datetime
from typing import Optional
from attrs import frozen, field
from drukarnia_api.models.relationship import AuthorRelationshipsModel
from drukarnia_api.models.tag import TagModel
from drukarnia_api.models.base import BaseModel
from drukarnia_api.models.article.from_author import ArticleFromAuthorModel
from drukarnia_api.models.article.extended_article_card import ExtendedCardArticleModel
from drukarnia_api.models.author.article_author import ArticleAuthorModel
from drukarnia_api.models.comment import CommentModel


@frozen
class ArticleModel(BaseModel):
    _id: str
    title: str
    seoTitle: str
    description: str
    picture: Optional[str]
    thumbPicture: Optional[str]
    mainTag: str
    mainTagSlug: str
    mainTagId: str
    tags: list[TagModel] = field(
        converter=TagModel.from_json,
    )
    ads: bool
    index: bool
    sensetive: bool
    canonical: Optional[str]
    likeNum: int
    commentNum: int
    readTime: int
    slug: str
    createdAt: datetime = field(
        converter=datetime.fromisoformat,
    )
    authorArticles: list[ArticleFromAuthorModel] = field(
        converter=ArticleFromAuthorModel.from_json
    )
    content: dict
    owner: ArticleAuthorModel = field(
        converter=ArticleAuthorModel.from_json
    )
    isLiked: bool = field(
        converter=bool
    )
    isBookmarked: bool
    relationships: AuthorRelationshipsModel = field(
        converter=AuthorRelationshipsModel.from_json
    )
    comments: list[CommentModel] = field(
        converter=CommentModel.from_json,
    )
    recommendedArticles: list[ExtendedCardArticleModel] = field(
        converter=ExtendedCardArticleModel.from_json
    )

