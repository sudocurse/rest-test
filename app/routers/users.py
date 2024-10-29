from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

memory_db = {}

router = APIRouter()


class User(BaseModel):
    id: int
    name: str
    email: str


@router.get("/users/", tags=["users"])
async def get_users():
    return list(memory_db.values())


@router.post("/users/", tags=["users"])
async def create_user(user: User):
    user = jsonable_encoder(user)
    memory_db[user["id"]] = user
    return user


@router.get("/users/{id}", tags=["users"])
async def get_user(id: int):
    if id not in memory_db:
        return None
    return memory_db[id]


@router.put("/users/{id}", tags=["users"])
async def update_user(id: int, user: User):
    if id not in memory_db:
        return None
    memory_db[id] = user
    return user


@router.delete("/users/{id}", tags=["users"])
async def delete_user(id: int):
    if id not in memory_db:
        return None
    del memory_db[id]
    return None
