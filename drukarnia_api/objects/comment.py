from aiohttp import ClientSession

from drukarnia_api.objects.base_object import DrukarniaElement
from drukarnia_api.shortcuts import data2authors, data2comments

from datetime import datetime
from typing import TYPE_CHECKING, Tuple, Dict

if TYPE_CHECKING:  # always False, used for type hints
    from drukarnia_api.objects.author import Author


class Comment(DrukarniaElement):
    async def reply(self, comment_text: str) -> str:
        """
        Posts a reply to a comment and returns the ID of the new comment.

        Parameters:
            comment_text (str): The text of the comment to be posted as a reply.

        Returns:
            str: The ID of the new comment.
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

    @DrukarniaElement.requires_attributes(['article_id', 'comment_id'])
    async def get_replies(self,
                          create_comments: bool = True) -> Tuple['Comment'] or Tuple[Dict]:
        """
        Deletes a comment from the article.
        """

        replies = await self.request(
            'get',
            f'/api/articles/{await self.article_id}/comments/{await self.comment_id}/replies',
            output='json'
        )

        if create_comments:
            replies = await data2comments(replies, session=self.session)

        return replies

    @DrukarniaElement.requires_attributes(['article_id'])
    async def like_comment(self, unlike: bool = False) -> None:
        """
        Likes or unlikes a comment based on the 'delete' parameter.

        Parameters:
            unlike (bool, optional): If True, the comment will be unliked.
            If False, the comment will be liked. Default is False.
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
        """
        Property to access the creation date of the comment.

        Returns:
            datetime: The creation date of the comment.
        """

        return self._access_data('createdAt')

    @property
    @DrukarniaElement.type_decorator(bool)
    async def hidden(self) -> bool:
        """
        Property to check if the comment is hidden by the author.

        Returns:
            bool: True if the comment is hidden, False otherwise.
        """
        return self._access_data('hiddenByAuthor')

    @property
    @DrukarniaElement.type_decorator(bool)
    async def is_blocked(self) -> bool:
        """
        Property to check if the comment is blocked.

        Returns:
            bool: True if the comment is blocked, False otherwise.
        """
        return self._access_data('isBlocked')

    @property
    @DrukarniaElement.type_decorator(bool)
    async def is_liked(self) -> bool:
        """
        Property to check if the comment is liked by you.

        Returns:
            bool: True if the comment is liked, False otherwise.
        """
        return self._access_data('isLiked')

    @property
    @DrukarniaElement.type_decorator(int)
    async def number_of_replies(self) -> int:
        """
        Property to get the number of replies to the comment.

        Returns:
            int: The number of replies to the comment.
        """
        return self._access_data('replyNum')

    @property
    @DrukarniaElement.type_decorator(int)
    async def number_of_likes(self) -> int:
        """
        Property to get the number of likes on the comment.

        Returns:
            int: The number of likes on the comment.
        """
        return self._access_data('likesNum')

    @property
    @DrukarniaElement.type_decorator(str)
    async def article_id(self) -> str or None:
        """
        Property to get the ID of the associated article.

        Returns:
            str or None: The ID of the associated article if available, otherwise None.
        """
        return self._access_data('article')

    @property
    async def owner(self) -> 'Author':
        """
        Property to get the owner (author) of the comment.

        Returns:
            Author: The Author object representing the owner of the comment.
        """
        author = await data2authors([self._access_data('owner', [])], self.session)
        return author[0] if author else None

    @property
    @DrukarniaElement.type_decorator(str)
    async def text(self) -> str:
        """
        Property to get the text of the comment.

        Returns:
            str: The text of the comment.
        """
        return self._access_data('comment')

    @property
    @DrukarniaElement.type_decorator(str)
    async def owner_id(self) -> str or None:
        """
        Property to get the ID of the owner (author) of the comment.

        Returns:
            str or None: The ID of the owner (author) of the comment if available, otherwise None.
        """
        return self._access_data('owner', {}).get('_id', None)

    @property
    @DrukarniaElement.type_decorator(str)
    async def comment_id(self) -> str:
        """
        Retrieves the ID of the comment.

        Returns:
            str: The ID of the comment.
        """
        return self._access_data('_id')

    @staticmethod
    async def from_records(session: ClientSession, new_data: dict) -> 'Comment':
        """
        Creates a Comment instance from records.

        Parameters:
            session (ClientSession): The aiohttp ClientSession object to use for API requests.
            new_data (dict): A dictionary containing the data for the new comment.

        Returns:
            Comment: The newly created Comment instance.
        """
        new_comment = Comment(session=session)
        new_comment._update_data(new_data)

        return new_comment
