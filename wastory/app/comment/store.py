from functools import cache
from typing import Annotated
from sqlalchemy.orm import selectinload
from sqlalchemy import select,and_,func
from wastory.app.comment.errors import CommentNotFoundError,NotOwnerError
from wastory.app.user.models import User
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION
from wastory.app.article.models import Article
from wastory.app.comment.models import Comment

class CommentStore:
    async def get_comment_by_id(self,id:int)->Comment|None:
        get_comment_query=select(Comment).filter(Comment.id==id)
        comment=await SESSION.scalar(get_comment_query)
        return comment

    async def get_article_comments(
        self, article_id: int, page: int, per_page: int
    ) -> list[Comment]:
        offset_val = (page - 1) * per_page

        stmt = (
            select(Comment)
            .filter(Comment.article_id == article_id, Comment.level == 1)
            .options(selectinload(Comment.children))  # 자식 로드
            .offset(offset_val)
            .limit(per_page)
        )
        results = await SESSION.scalars(stmt)
        return list(results)

    async def get_total_level1_article_comments_count(self, article_id: int) -> int:
        stmt = select(func.count(Comment.id)).filter(
            Comment.article_id == article_id,
            Comment.level == 1
        )
        count = await SESSION.scalar(stmt)
        return count or 0


    async def get_guestbook_comments(
        self, blog_id: int, page: int, per_page: int
    ) -> list[Comment]:
        offset_val = (page - 1) * per_page

        stmt = (
            select(Comment)
            .filter(Comment.blog_id == blog_id, Comment.level == 1)
            .options(selectinload(Comment.children))  # 자식 로드
            .offset(offset_val)
            .limit(per_page)
        )
        results = await SESSION.scalars(stmt)
        return list(results)

    async def get_total_level1_guestbook_comments_count(self, blog_id: int) -> int:
        stmt = select(func.count(Comment.id)).filter(
            Comment.blog_id == blog_id,
            Comment.level == 1
        )
        count = await SESSION.scalar(stmt)
        return count or 0


    @transactional
    async def create_article_comment_1(
        self, content:str,secret:int,user:User,article_id:int
        )->Comment:
            print(content)
            print(user.username)
            print(secret)
            comment= Comment(
                content=content,
                level=1,
                secret=secret,
                user_id=user.id,
                user_name=user.username,
                article_id=article_id,
                parent_id=None
                )
            SESSION.add(comment)
            print(comment)
            await SESSION.flush()
            await SESSION.refresh(comment)
            return comment
        
    @transactional
    async def create_article_comment_2(
        self, content:str,secret:int,user:User,article_id:int,parent_id:int
        )->Comment:
            comment= Comment(
                content=content,
                level=2,
                secret=secret,
                user_id=user.id,
                user_name=user.username,
                article_id=article_id,
                parent_id=parent_id
            )
            parent_comment=await self.get_comment_by_id(parent_id)
            if not parent_comment:
                raise CommentNotFoundError()
            comment.parent = parent_comment
            SESSION.add(comment)
            await SESSION.flush()
            await SESSION.refresh(comment)
            return comment

    @transactional
    async def create_guestbook_comment_1(
        self, content:str,secret:int,user:User,blog_id:int
        )->Comment:
            print(content)
            print(user.username)
            print(secret)
            comment= Comment(
                content=content,
                level=1,
                secret=secret,
                user_id=user.id,
                user_name=user.username,
                blog_id=blog_id,
                parent_id=None
                )
            SESSION.add(comment)
            print(comment)
            await SESSION.flush()
            await SESSION.refresh(comment)
            return comment
        
    @transactional
    async def create_guestbook_comment_2(
        self, content:str,secret:int,user:User,blog_id:int,parent_id:int
        )->Comment:
            comment= Comment(
                content=content,
                level=2,
                secret=secret,
                user_id=user.id,
                user_name=user.username,
                blog_id=blog_id,
                parent_id=parent_id
            )
            parent_comment=await self.get_comment_by_id(parent_id)
            if not parent_comment:
                raise CommentNotFoundError()
            comment.parent = parent_comment
            SESSION.add(comment)
            await SESSION.flush()
            await SESSION.refresh(comment)
            return comment


    @transactional
    async def update_comment(
        self,
        user:User,
        comment_id: int,
        content:str
    ) -> Comment:
        comment = await self.get_comment_by_id(comment_id)
        
        
        if comment is None:
            raise CommentNotFoundError()

        if comment.user_id!=user.id:
            raise NotOwnerError()

        if content is not None:
            comment.content=content
        

        SESSION.merge(comment)
        await SESSION.flush()
        await SESSION.refresh(comment)

        return comment

    @transactional
    async def delete_comment(self, user: User, comment_id: int) -> None:
        comment = await self.get_comment_by_id(comment_id)

        if comment is None:
            raise CommentNotFoundError()

        
        if comment.user_id!=user.id:
            raise NotOwnerError()

        await SESSION.delete(comment)
        await SESSION.flush()

    