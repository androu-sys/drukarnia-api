from enum import StrEnum


class DrukarniaEndpoints(StrEnum):
    BlockAuthor = "/api/relationships/block/{author_id}"
    BlockTag = "/api/preferences/tags/{tag_id}/block"
    BookmarkArticle = "/api/articles/bookmarks"
    CreateNewBookmark = "/api/articles/bookmarks/lists"
    DeleteBookmark = "/api/articles/bookmarks/lists/{bookmark_id}"
    UnBookmarkArticle = "/api/articles/{article_id}/bookmarks"
    ChangeUserGeneralInfo = "/api/users"
    ChangeUserEmail = "/api/users/login/email"
    ChangeUserPassword = "/api/users/login/password"
    DeleteComment = "/api/articles/{article_id}/comments/{comment_id}"

