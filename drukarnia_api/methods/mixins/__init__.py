from drukarnia_api.methods.mixins.with_article import MixinWithArticleId, MixinWithArticleSlug
from drukarnia_api.methods.mixins.with_author import MixinWithAuthorId, MixinWithUsername
from drukarnia_api.methods.mixins.with_bool_option import (
    MixinWithPreviewOption,
    MixinWithRelationsOption,
    MixinWithUnblockOption,
    MixinWithUnbookmarkOption,
    MixinWithUnlikeOption,
    MixinWithUnsubscribeOption,
)
from drukarnia_api.methods.mixins.with_comment import MixinWithCommentId, MixinWithCommentText
from drukarnia_api.methods.mixins.with_pagination import MixinWithPagination
from drukarnia_api.methods.mixins.with_password import MixinWithCurrentPassword
from drukarnia_api.methods.mixins.with_query import MixinWithQuery
from drukarnia_api.methods.mixins.with_section import MixinWithSectionId, MixinWithSectionName
from drukarnia_api.methods.mixins.with_tag import MixinWithTagId, MixinWithTagSlug

__all__ = [
    "MixinWithArticleId",
    "MixinWithCommentId",
    "MixinWithCommentText",
    "MixinWithUnlikeOption",
    "MixinWithPagination",
    "MixinWithAuthorId",
    "MixinWithTagId",
    "MixinWithUnblockOption",
    "MixinWithUnbookmarkOption",
    "MixinWithPreviewOption",
    "MixinWithRelationsOption",
    "MixinWithArticleSlug",
    "MixinWithUsername",
    "MixinWithSectionId",
    "MixinWithSectionName",
    "MixinWithTagSlug",
    "MixinWithQuery",
    "MixinWithUnsubscribeOption",
    "MixinWithCurrentPassword",
]
