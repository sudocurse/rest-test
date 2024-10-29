from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid

users_db = {}

router = APIRouter()


class User(BaseModel):
    id: uuid.UUID
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str


@router.get("/users/", tags=["users"])
async def get_users():
    return list(users_db.values())


@router.post("/users/", tags=["users"], response_model=User)
async def create_user(user: UserCreate):
    user = User(id=uuid.uuid4(), **user.dict())
    users_db[user.id] = user
    return user


@router.get("/users/{id}", tags=["users"])
async def get_user(id: uuid.UUID):
    if id not in users_db:
        return JSONResponse(status_code=404, content={f"error": "User id {id} not found"})
    return users_db[id]


@router.put("/users/{id}", tags=["users"])
async def update_user(id: uuid.UUID, user: UserCreate):
    if id not in users_db:
        return JSONResponse(status_code=404, content={f"error": "User id {id} not found"})
    user = User(id=id, **user.dict())
    users_db[id] = user
    return user


@router.delete("/users/{id}", tags=["users"])
async def delete_user(id: uuid.UUID):
    if id not in users_db:
        return JSONResponse(status_code=404, content={f"error": "User id {id} not found"})
    del users_db[id]
    return JSONResponse(status_code=204, content={"status": "success"})
