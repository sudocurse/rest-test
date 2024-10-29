from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from .users import users_db
from .utils import ErrorResponse

import uuid

posts_db = {}

router = APIRouter()


class Post(BaseModel):
    id: int
    title: str
    content: str
    user_id: uuid.UUID


class PostCreate(BaseModel):
    title: str
    content: str
    user_id: uuid.UUID


@router.get("/posts/", tags=["posts"], responses={200: {"model": Post}})
async def get_posts():
    return list(posts_db.values())


@router.post("/posts/", tags=["posts"], responses={200: {"model": Post}})
async def create_post(post: PostCreate):
    if post.user_id not in users_db:
        raise HTTPException(status_code=404, detail=f"User id {post.user_id} not found")
    post = Post(id=len(posts_db) + 1, **post.dict())
    posts_db[post.id] = post
    return post


@router.get(
    "/posts/{id}",
    tags=["posts"],
    responses={
        200: {"model": Post},
        404: {"model": ErrorResponse}})
async def get_post(id: int):
    print(posts_db)
    if id not in posts_db:
        raise HTTPException(status_code=404, detail=f"Post id {id} not found")
    return posts_db[id]


@router.put("/posts/{id}",
            tags=["posts"],
            responses={
                200: {"model": Post},
                404: {"model": ErrorResponse}})
async def update_post(id: int, post: PostCreate):
    if id not in posts_db:
        raise HTTPException(status_code=404, detail=f"Post id {id} not found")
    post = Post(id=id, **post.dict())
    posts_db[id] = post
    return post


@router.delete(
    "/posts/{id}",
    tags=["posts"],
    responses={
        204: {"description": "Post deleted"},  # No 'model' or 'content'
        404: {"model": ErrorResponse, "description": "Post not found"},
    },
    status_code=204,
)
async def delete_post(id: int):
    print(posts_db)
    if id not in posts_db:
        raise HTTPException(status_code=404, detail=f"Post id {id} not found")
    del posts_db[id]
    return
