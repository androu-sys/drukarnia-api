from attrs import frozen, field
from drukarnia_api.models.author.author_card import AuthorCardModel
from drukarnia_api.models.article.article_card import ArticleCardModel


@frozen
class ExtendedCardArticleModel(ArticleCardModel):
    owner: AuthorCardModel = field(
        converter=AuthorCardModel.from_json
    )
