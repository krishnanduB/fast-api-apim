from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float | None = None

@router.get("/")
def read_items(skip: int = 0, limit: int = 10, search: str | None = None):
    return {
        "query_params": {"skip": skip, "limit": limit, "search": search},
        "items": [{"item_id": 1, "name": "Item 1"}, {"item_id": 2, "name": "Item 2"}]
    }

@router.get("/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@router.post("/")
def create_item(item: Item):
    return {"message": f"Item {item.name} created successfully", "item": item}

@router.put("/{item_id}")
def update_item(item_id: int, item: Item):
    return {"message": f"Item {item_id} updated successfully", "item_id": item_id, "item": item}

@router.patch("/{item_id}")
def partially_update_item(item_id: int, item: ItemUpdate):
    return {"message": f"Item {item_id} partially updated successfully", "item_id": item_id, "item": item}

@router.delete("/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted successfully", "item_id": item_id}
