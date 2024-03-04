from typing import TYPE_CHECKING, Iterable

from drukarnia_api.methods import (
    BlockAuthor,
    BlockTag,
    BookmarkArticle,
    ChangeAuthorInfo,
    ChangeEmail,
    ChangePassword,
    CreateSection,
    DeleteComment,
    DeleteSection,
    FindArticle,
    FindAuthor,
    FindTags,
    GetArticle,
    GetAuthor,
    GetBlockedAuthors,
    GetCommentReplies,
    GetFollowers,
    GetFollowings,
    GetNotifications,
    GetReadsHistory,
    GetSections,
    GetTag,
    GetTagRelatedArticles,
    GetTagRelatedAuthors,
    GetTagRelatedTags,
    LikeArticle,
    LikeComment,
    Login,
    PostComment,
    ReplyToComment,
    SubscribeToAuthor,
    SubscribeToTag,
)
from drukarnia_api.models import (
    ArticleModel,
    AuthorModel,
    CommentModel,
    NotificationModel,
    SectionModel,
    TagModel,
)
from drukarnia_api.network import API

if TYPE_CHECKING:
    from drukarnia_api.dto import UserInfoUpdate


class Drukarnia(API):
    async def reply_to_comment(
            self,
            article_id: str | ArticleModel,
            comment_id: str | CommentModel,
            author_id: str | AuthorModel,
            comment_text: str | CommentModel,
    ) -> CommentModel:
        if isinstance(article_id, ArticleModel):
            article_id = article_id.id_
        if isinstance(comment_text, CommentModel):
            comment_text = comment_text.comment
        if isinstance(comment_id, CommentModel):
            comment_id = comment_id.id_
        if isinstance(author_id, AuthorModel):
            author_id = author_id.id_
        return await self(ReplyToComment(
            article_id=article_id,
            comment_id=comment_id,
            author_id=author_id,
            comment_text=comment_text,
        ))

    async def change_email(
        self,
        current_password: str,
        new_email: str,
    ) -> None:
        return await self(ChangeEmail(
            current_password=current_password,
            new_email=new_email,
        ))

    async def login(
        self,
        email: str,
        current_password: str,
    ) -> AuthorModel:
        return await self(Login(
            email=email,
            current_password=current_password,
        ))

    async def get_followings(
        self,
        author_id: AuthorModel | str,
        page: int = 1,
    ) -> Iterable[AuthorModel]:
        if isinstance(author_id, AuthorModel):
            author_id = author_id.id_

        return await self(GetFollowings(
            author_id=author_id,
            page=page,
        ))

    async def get_tag_related_articles(
        self,
        tag_id: str | TagModel,
        page: int = 1,
    ) -> Iterable[ArticleModel]:
        if isinstance(tag_id, TagModel):
            tag_id = tag_id.id_
        return await self(GetTagRelatedArticles(
            tag_id=tag_id,
            page=page,
        ))

    async def get_reads_history(
        self,
        page: int = 1,
    ) -> Iterable[ArticleModel]:
        return await self(GetReadsHistory(
            page=page,
        ))

    async def get_followers(
        self,
        author_id: AuthorModel | str,
        page: int = 1,
    ) -> Iterable[AuthorModel]:
        if isinstance(author_id, AuthorModel):
            author_id = author_id.id_

        return await self(GetFollowers(
            author_id=author_id,
            page=page,
        ))

    async def block_tag(
        self,
        tag_id: str | TagModel,
        unblock: bool = False
    ) -> None:
        if isinstance(tag_id, TagModel):
            tag_id = tag_id.id_

        await self(BlockTag(
            tag_id=tag_id,
            unblock=unblock,
        ))

    async def change_password(
        self,
        current_password: str,
        new_password: str,
    ) -> None:
        await self(ChangePassword(
            current_password=current_password,
            new_password=new_password
        ))

    async def subscribe(
        self,
        author_id: AuthorModel | str,
        unsubscribe: bool = False,
    ) -> None:

        if isinstance(author_id, AuthorModel):
            author_id = author_id.id_

        return await self(SubscribeToAuthor(
            author_id=author_id,
            unsubscribe=unsubscribe,
        ))

    async def find_articles(
        self,
        query: str,
        page: int = 1,
    ) -> Iterable[ArticleModel]:
        return await self(FindArticle(
            query=query,
            page=page,
        ))

    async def get_tag_related_tags(
        self,
        tag_id: str | TagModel,
        page: int = 1,
    ) -> Iterable[TagModel]:
        if isinstance(tag_id, TagModel):
            tag_id = tag_id.id_
        return await self(GetTagRelatedTags(
            tag_id=tag_id,
            page=page,
        ))

    async def subscribe_to_tag(
        self,
        tag_id: str | TagModel,
        unsubscribe: bool = False
    ) -> None:
        if isinstance(tag_id, TagModel):
            tag_id = tag_id.id_
        return await self(SubscribeToTag(
            tag_id=tag_id,
            unsubscribe=unsubscribe,
        ))

    async def delete_comment(
        self,
        article_id: str | ArticleModel,
        comment_id: str | CommentModel
    ) -> None:
        if isinstance(article_id, ArticleModel):
            article_id = article_id.id_
        if isinstance(comment_id, CommentModel):
            comment_id = comment_id.id_
        return await self(DeleteComment(
            article_id=article_id,
            comment_id=comment_id,
        ))

    async def get_blocked_authors(
        self,
    ) -> Iterable[AuthorModel]:
        return await self(GetBlockedAuthors())

    async def block_author(
        self,
        author_id: str | AuthorModel,
        unblock: bool = False
    ) -> None:
        if isinstance(author_id, AuthorModel):
            author_id = author_id.id_
        return await self(BlockAuthor(
            author_id=author_id,
            unblock=unblock,
        ))

    async def get_notifications(
        self,
        page: int = 1,
    ) -> Iterable[NotificationModel]:
        return await self(GetNotifications(
            page=page,
        ))

    async def get_article(
        self,
        article_slug: str | ArticleModel
    ) -> ArticleModel:
        if isinstance(article_slug, ArticleModel):
            article_slug = ArticleModel.slug

        return await self(GetArticle(
            article_slug=article_slug,
        ))

    async def delete_section(
        self,
        section_id: str | SectionModel
    ) -> None:
        if isinstance(section_id, SectionModel):
            section_id = section_id.id_

        return await self(DeleteSection(
            section_id=section_id,
        ))

    async def create_section(
        self,
        section_name: str | SectionModel,
    ) -> SectionModel:
        if isinstance(section_name, SectionModel):
            section_name = SectionModel.name
        return await self(CreateSection(
            section_name=section_name,
        ))

    async def post_comment(
        self,
        article_id: str | ArticleModel,
        comment_text: str | CommentModel,
    ) -> CommentModel:
        if isinstance(article_id, ArticleModel):
            article_id = article_id.id_
        if isinstance(comment_text, CommentModel):
            comment_text = CommentModel.comment
        return await self(PostComment(
            article_id=article_id,
            comment_text=comment_text,
        ))

    async def like_article(
        self,
        article_id: str | ArticleModel,
        n_likes: int = 1
    ) -> None:
        if isinstance(article_id, ArticleModel):
            article_id = article_id.id_
        return await self(LikeArticle(
            article_id=article_id,
            n_likes=n_likes,
        ))

    async def get_comment_replies(
        self,
        article_id: str | ArticleModel,
        comment_id: str | CommentModel,
    ) -> Iterable[CommentModel]:
        if isinstance(article_id, ArticleModel):
            article_id = article_id.id_
        if isinstance(comment_id, CommentModel):
            comment_id = comment_id.id_
        return await self(GetCommentReplies(
            article_id=article_id,
            comment_id=comment_id,
        ))

    async def change_author_info(
        self,
        config: "UserInfoUpdate",
    ) -> None:
        return await self(ChangeAuthorInfo(
            config=config,
        ))

    async def get_tag_related_authors(
        self,
        tag_id: str | TagModel,
    ) -> Iterable[AuthorModel]:
        if isinstance(tag_id, TagModel):
            tag_id = tag_id.id_
        return await self(GetTagRelatedAuthors(
            tag_id=tag_id,
        ))

    async def bookmark_article(
        self,
        article_id: str | ArticleModel,
        section_id: str | SectionModel,
        unbookmark: bool = False
    ) -> None:
        if isinstance(article_id, ArticleModel):
            article_id = article_id.id_
        if isinstance(section_id, SectionModel):
            section_id = section_id.id_
        return await self(BookmarkArticle(
            article_id=article_id,
            section_id=section_id,
            unbookmark=unbookmark,
        ))

    async def get_author(
        self,
        username: str | AuthorModel,
    ) -> AuthorModel:
        if isinstance(username, AuthorModel):
            username = AuthorModel.username
        return await self(GetAuthor(
            username=username,
        ))

    async def like_comment(
        self,
        article_id: str | ArticleModel,
        comment_id: str | CommentModel,
        unlike: bool = False
    ) -> None:
        if isinstance(article_id, ArticleModel):
            article_id = article_id.id_
        if isinstance(comment_id, CommentModel):
            comment_id = comment_id.id_
        return await self(LikeComment(
            article_id=article_id,
            comment_id=comment_id,
            unlike=unlike,
        ))

    async def find_tags(
        self,
        query: str,
        page: int = 1,
    ) -> Iterable[TagModel]:
        return await self(FindTags(
            query=query,
            page=page,
        ))

    async def get_tag(
        self,
        tag_slug: str | TagModel,
    ) -> TagModel:
        if isinstance(tag_slug, TagModel):
            tag_slug = TagModel.slug
        return await self(GetTag(
            tag_slug=tag_slug,
        ))

    async def find_author(
        self,
        query: str,
        with_relations: bool = False,
        page: int = 1,
    ) -> Iterable[AuthorModel]:
        return await self(FindAuthor(
            query=query,
            with_relations=with_relations,
            page=page,
        ))

    async def get_sections(
        self,
        preview: bool = False,
    ) -> Iterable[SectionModel]:
        return await self(GetSections(
            preview=preview,
        ))
