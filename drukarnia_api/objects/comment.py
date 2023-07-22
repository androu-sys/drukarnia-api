from datetime import datetime

from aiohttp import ClientSession

from drukarnia_api.drukarnia_base import DrukarniaElement
from drukarnia_api.shortcuts import data2authors

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # always False, used for type hints
    from drukarnia_api.author import Author


class Comment(DrukarniaElement):
    @DrukarniaElement._is_authenticated
    async def reply(self, comment_text: str) -> str:
        """
        Posts a reply to a comment and returns the ID of the new comment.
        """

        new_comment_id = await self.request(
            'post',
            f'/api/articles/{self.article_id}/comments/{self.comment_id}/replies',
            data={
                "comment": comment_text,
                "replyToComment": self.comment_id,
                "rootComment": self.comment_id,   # not sure
                "rootCommentOwner": self.owner_id,
                "replyToUser": self.owner_id,
            },
            output='read'
        )

        return new_comment_id.decode('utf-8')

    @DrukarniaElement._is_authenticated
    async def delete(self) -> None:
        """
        Deletes a comment from the article.
        """

        await self.request('delete', f'/api/articles/{self.article_id}/comments/{self.comment_id}')

    @DrukarniaElement._control_attr('article_id')
    @DrukarniaElement._is_authenticated
    async def like_comment(self, unlike: bool = False) -> None:
        """
        Likes or unlikes a comment based on the 'delete' parameter.
        """

        if unlike:
            await self.request('delete', f'/api/articles/{self.article_id}/comments/{self.comment_id}/likes')

        else:
            await self.request('post', f'/api/articles/{self.article_id}/comments/{self.comment_id}/likes')

    @property
    def created_at(self) -> datetime:
        return self._get_datetime_from_author_data('createdAt')

    @property
    def hidden(self) -> bool:
        return self._get_basetype_from_data('hiddenByAuthor', bool, False)

    @property
    def is_blocked(self) -> bool:
        return self._get_basetype_from_data('isBlocked', bool, False)

    @property
    def is_liked(self) -> bool:
        return self._get_basetype_from_data('isLiked', bool, False)

    @property
    def number_of_replies(self) -> int:
        return self._get_basetype_from_data('replyNum', int, 0)

    @property
    def number_of_likes(self) -> int:
        return self._get_basetype_from_data('likesNum', int, 0)

    @property
    def article_id(self) -> str or None:
        return self._access_data('article', None)

    @property
    async def owner(self) -> 'Author':
        author = await data2authors([self._access_data('owner', [])], self.session)
        return author[0] if author else None

    @property
    def text(self) -> str:
        return self._get_basetype_from_data('comment', str)

    @property
    def owner_id(self) -> str or None:
        return self._access_data('owner', {}).get('_id', None)

    @property
    def comment_id(self) -> str:
        """
        Retrieves the ID of the article.
        """
        return self._get_basetype_from_data('_id', str)

    @staticmethod
    async def from_records(session: ClientSession, new_data: dict) -> 'Comment':
        """
        Creates an Article instance from records.
        """
        new_comment = Comment(session=session)
        new_comment._update_data(new_data)

        return new_comment
