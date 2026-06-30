from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.storage import read_data, write_data
import os

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

USERS_FILE = os.path.join("data", "users.json")

@router.get("/")
def read_users(skip: int = 0, limit: int = 10, is_active: bool | None = None):
    users = read_data(USERS_FILE)
    if is_active is not None:
        users = [user for user in users if user.get("disabled") == (not is_active)]
    return {
        "query_params": {"skip": skip, "limit": limit, "is_active": is_active},
        "users": users[skip : skip + limit]
    }

@router.get("/{user_id}")
def read_user(user_id: int):
    users = read_data(USERS_FILE)
    for user in users:
        if user.get("user_id") == user_id:
            return {"user_id": user_id, "user": user}
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/")
def create_user(user: User):
    users = read_data(USERS_FILE)
    new_id = max([u.get("user_id", 0) for u in users] + [0]) + 1
    new_user = user.model_dump()
    new_user["user_id"] = new_id
    users.append(new_user)
    write_data(USERS_FILE, users)
    return {"message": f"User {user.username} created successfully", "user": new_user}

@router.put("/{user_id}")
def update_user(user_id: int, user: User):
    users = read_data(USERS_FILE)
    for idx, existing_user in enumerate(users):
        if existing_user.get("user_id") == user_id:
            updated_user = user.model_dump()
            updated_user["user_id"] = user_id
            users[idx] = updated_user
            write_data(USERS_FILE, users)
            return {"message": f"User {user_id} updated successfully", "user_id": user_id, "user": updated_user}
    raise HTTPException(status_code=404, detail="User not found")

@router.patch("/{user_id}")
def partially_update_user(user_id: int, user: UserUpdate):
    users = read_data(USERS_FILE)
    for idx, existing_user in enumerate(users):
        if existing_user.get("user_id") == user_id:
            update_data = user.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                existing_user[key] = value
            users[idx] = existing_user
            write_data(USERS_FILE, users)
            return {"message": f"User {user_id} partially updated successfully", "user_id": user_id, "user": existing_user}
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}")
def delete_user(user_id: int):
    users = read_data(USERS_FILE)
    for idx, existing_user in enumerate(users):
        if existing_user.get("user_id") == user_id:
            users.pop(idx)
            write_data(USERS_FILE, users)
            return {"message": f"User {user_id} deleted successfully", "user_id": user_id}
    raise HTTPException(status_code=404, detail="User not found")
