from aiohttp import ClientSession

from drukarnia_api.objects.base_object import DrukarniaElement
from drukarnia_api.shortcuts import data2authors

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # always False, used for type hints
    from drukarnia_api.objects.author import Author


class Comment(DrukarniaElement):
    async def reply(self, comment_text: str) -> str:
        """
        Posts a reply to a comment and returns the ID of the new comment.
        """

        new_comment_id = await self.request(
            'post',
            f'/api/articles/{await self.article_id}/comments/{await self.comment_id}/replies',
            data={
                "comment": comment_text,
                "replyToComment": await self.comment_id,
                "rootComment": await self.comment_id,   # not sure
                "rootCommentOwner": await self.owner_id,
                "replyToUser": await self.owner_id,
            },
            output='read'
        )

        return new_comment_id.decode('utf-8')

    async def delete(self) -> None:
        """
        Deletes a comment from the article.
        """

        await self.request(
            'delete',
            f'/api/articles/{await self.article_id}/comments/{await self.comment_id}')

    @DrukarniaElement.requires_attributes(['article_id'])
    async def like_comment(self, unlike: bool = False) -> None:
        """
        Likes or unlikes a comment based on the 'delete' parameter.
        """

        if unlike:
            await self.request(
                'delete',
                f'/api/articles/{await self.article_id}/comments/{await self.comment_id}/likes')

        else:
            await self.request(
                'post',
                f'/api/articles/{await self.article_id}/comments/{await self.comment_id}/likes')

    @property
    @DrukarniaElement.type_decorator(datetime)
    async def created_at(self) -> datetime:
        return self._access_data('createdAt')

    @property
    @DrukarniaElement.type_decorator(bool)
    async def hidden(self) -> bool:
        return self._access_data('hiddenByAuthor')

    @property
    @DrukarniaElement.type_decorator(bool)
    async def is_blocked(self) -> bool:
        return self._access_data('isBlocked')

    @property
    @DrukarniaElement.type_decorator(bool)
    async def is_liked(self) -> bool:
        return self._access_data('isLiked')

    @property
    @DrukarniaElement.type_decorator(int)
    async def number_of_replies(self) -> int:
        return self._access_data('replyNum')

    @property
    @DrukarniaElement.type_decorator(int)
    async def number_of_likes(self) -> int:
        return self._access_data('likesNum')

    @property
    @DrukarniaElement.type_decorator(str)
    async def article_id(self) -> str or None:
        return self._access_data('article')

    @property
    async def owner(self) -> 'Author':
        author = await data2authors([self._access_data('owner', [])], self.session)
        return author[0] if author else None

    @property
    @DrukarniaElement.type_decorator(str)
    async def text(self) -> str:
        return self._access_data('comment')

    @property
    @DrukarniaElement.type_decorator(str)
    async def owner_id(self) -> str or None:
        return self._access_data('owner', {}).get('_id', None)

    @property
    @DrukarniaElement.type_decorator(str)
    async def comment_id(self) -> str:
        """
        Retrieves the ID of the article.
        """
        return self._access_data('_id')

    @staticmethod
    async def from_records(session: ClientSession, new_data: dict) -> 'Comment':
        """
        Creates an Article instance from records.
        """
        new_comment = Comment(session=session)
        new_comment._update_data(new_data)

        return new_comment
