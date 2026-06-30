from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

class User(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    disabled: bool | None = False

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

@router.get("/")
def read_users(skip: int = 0, limit: int = 10, is_active: bool | None = None):
    return {
        "query_params": {"skip": skip, "limit": limit, "is_active": is_active},
        "users": [{"user_id": 1, "username": "user1"}, {"user_id": 2, "username": "user2"}]
    }

@router.get("/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id, "email": f"user{user_id}@example.com"}

@router.post("/")
def create_user(user: User):
    return {"message": f"User {user.username} created successfully", "user": user}

@router.put("/{user_id}")
def update_user(user_id: int, user: User):
    return {"message": f"User {user_id} updated successfully", "user_id": user_id, "user": user}

@router.patch("/{user_id}")
def partially_update_user(user_id: int, user: UserUpdate):
    return {"message": f"User {user_id} partially updated successfully", "user_id": user_id, "user": user}

@router.delete("/{user_id}")
def delete_user(user_id: int):
    return {"message": f"User {user_id} deleted successfully", "user_id": user_id}
