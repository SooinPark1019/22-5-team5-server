from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED,HTTP_204_NO_CONTENT

from wastory.app.user.models import User
comment_router = APIRouter()
from wastory.app.user.views import login_with_header
from wastory.app.comment.service import CommentService
from wastory.app.comment.dto.requests import CommentCreateRequest
from wastory.app.comment.dto.responses import CommentDetailResponse

@comment_router.post("/{article_id}/create", status_code=HTTP_201_CREATED)
async def create(
    user:Annotated[User,Depends(login_with_header)],
    comment_service: Annotated[CommentService, Depends()],
    comment_request: CommentCreateRequest,
    article_id:int,
)-> CommentDetailResponse:
    return await comment_service.create_comment(
        content=comment_request.content,
        level=comment_request.level,
        secret=comment_request.secret,
        user=user,
        article_id=article_id,
        parent_id=comment_request.parent_id
    )


@comment_router.get("/{article_id}", status_code=HTTP_200_OK)
async def create(
    user:Annotated[User,Depends(login_with_header)],
    article_id:int,
)-> None:
    return await None


@comment_router.patch("/{comment_id}", status_code=HTTP_200_OK)
async def create(
    user:Annotated[User,Depends(login_with_header)],
    comment_id:int,
)-> None:
    return await None

@comment_router.delete("/{comment_id}", status_code=HTTP_204_NO_CONTENT)
async def create(
    user:Annotated[User,Depends(login_with_header)],
    comment_id:int,
)-> None:
    return await None
