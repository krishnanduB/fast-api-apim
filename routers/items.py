from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.storage import read_data, write_data
import os

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    category: str

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float | None = None
    category: str | None = None

ITEMS_FILE = os.path.join("data", "items.json")

@router.get("/")
def read_items(skip: int = 0, limit: int = 10, search: str | None = None):
    items = read_data(ITEMS_FILE)
    if search:
        items = [item for item in items if search.lower() in item["name"].lower()]
    return {
        "query_params": {"skip": skip, "limit": limit, "search": search},
        "items": items[skip : skip + limit]
    }

@router.get("/{item_id}")
def read_item(item_id: int, q: str | None = None):
    items = read_data(ITEMS_FILE)
    for item in items:
        if item.get("item_id") == item_id:
            return {"item_id": item_id, "item": item, "q": q}
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("/")
def create_item(item: Item):
    items = read_data(ITEMS_FILE)
    new_id = max([i.get("item_id", 0) for i in items] + [0]) + 1
    new_item = item.model_dump()
    new_item["item_id"] = new_id
    items.append(new_item)
    write_data(ITEMS_FILE, items)
    return {"message": f"Item {item.name} created successfully", "item": new_item}

@router.put("/{item_id}")
def update_item(item_id: int, item: Item):
    items = read_data(ITEMS_FILE)
    for idx, existing_item in enumerate(items):
        if existing_item.get("item_id") == item_id:
            updated_item = item.model_dump()
            updated_item["item_id"] = item_id
            items[idx] = updated_item
            write_data(ITEMS_FILE, items)
            return {"message": f"Item {item_id} updated successfully", "item_id": item_id, "item": updated_item}
    raise HTTPException(status_code=404, detail="Item not found")

@router.patch("/{item_id}")
def partially_update_item(item_id: int, item: ItemUpdate):
    items = read_data(ITEMS_FILE)
    for idx, existing_item in enumerate(items):
        if existing_item.get("item_id") == item_id:
            update_data = item.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                existing_item[key] = value
            items[idx] = existing_item
            write_data(ITEMS_FILE, items)
            return {"message": f"Item {item_id} partially updated successfully", "item_id": item_id, "item": existing_item}
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/{item_id}")
def delete_item(item_id: int):
    items = read_data(ITEMS_FILE)
    for idx, existing_item in enumerate(items):
        if existing_item.get("item_id") == item_id:
            items.pop(idx)
            write_data(ITEMS_FILE, items)
            return {"message": f"Item {item_id} deleted successfully", "item_id": item_id}
    raise HTTPException(status_code=404, detail="Item not found")
