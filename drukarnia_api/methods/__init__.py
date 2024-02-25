from drukarnia_api.methods.base import BaseMethod
from drukarnia_api.methods.block_author import BlockAuthor
from drukarnia_api.methods.unblock_author import UnblockAuthor
from drukarnia_api.methods.block_tag import BlockTag
from drukarnia_api.methods.unblock_tag import UnblockTag
from drukarnia_api.methods.change_email import ChangeEmail
from drukarnia_api.methods.change_password import ChangePassword
from drukarnia_api.methods.change_author_info import ChangeAuthorInfo
from drukarnia_api.methods.create_bookmark import CreateBookmark
from drukarnia_api.methods.delete_bookmark import DeleteBookmark
from drukarnia_api.methods.get_author import GetAuthor
from drukarnia_api.methods.get_blocked import GetBlockedAuthors
from drukarnia_api.methods.get_followers import GetFollowers
from drukarnia_api.methods.get_followings import GetFollowings
from drukarnia_api.methods.get_author import GetAuthor
from drukarnia_api.methods.get_notifications import GetNotifications
from drukarnia_api.methods.get_reads_history import GetReadsHistory
from drukarnia_api.methods.get_bookmarks import GetBookmarks
from drukarnia_api.methods.login import Login
from drukarnia_api.methods.subscribe_author import SubscribeAuthor
from drukarnia_api.methods.unsubscribe_author import UnsubscribeAuthor
from drukarnia_api.methods.subscribe_tag import SubscribeTag
from drukarnia_api.methods.unsubscribe_tag import UnsubscribeTag
from drukarnia_api.methods.tag_data import GetTagData
from drukarnia_api.methods.get_articles_from_tag import GetArticlesFromTag
from drukarnia_api.methods.get_tag_related_authors import GetRelatedAuthorsFromTag
from drukarnia_api.methods.get_related_tags import GetRelatedTags


__all__ = [
    'BaseMethod',
    'BlockAuthor',
    'UnblockAuthor',
    'BlockTag',
    'UnblockTag',
    'ChangeEmail',
    'ChangePassword',
    'ChangeAuthorInfo',
    'CreateBookmark',
    'DeleteBookmark',
    'GetAuthor',
    'GetBlockedAuthors',
    'GetFollowers',
    'GetFollowings',
    'GetNotifications',
    'GetReadsHistory',
    'GetBookmarks',
    'Login',
    'SubscribeAuthor',
    'UnsubscribeAuthor',
    'SubscribeTag',
    'UnsubscribeTag',
    'GetTagData',
    'GetArticlesFromTag',
    'GetRelatedTags',
    'GetRelatedAuthorsFromTag'
]
