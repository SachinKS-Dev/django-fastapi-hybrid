from asgiref.sync import sync_to_async
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI()


class ItemSchema(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


# Define Django ORM functions with sync_to_async decorator
@sync_to_async
def get_items():
    from api.models import Item
    return list(Item.objects.all())


@sync_to_async
def get_item_by_id(item_id: int):
    from api.models import Item
    return Item.objects.filter(id=item_id).first()


@app.get("/items/", response_model=List[ItemSchema])
async def read_items():
    items = await get_items()
    return items


@app.post("/items/", response_model=ItemSchema)
async def create_item(item: ItemSchema):
    from api.models import Item
    new_item = Item(name=item.name, description=item.description)
    await sync_to_async(new_item.save)()
    return new_item


@app.get("/items/{item_id}/", response_model=ItemSchema)
async def read_item(item_id: int):
    item = await get_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}/", response_model=ItemSchema)
async def update_item(item_id: int, item: ItemSchema):
    existing_item = await get_item_by_id(item_id)
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    existing_item.name = item.name
    existing_item.description = item.description
    await sync_to_async(existing_item.save)()
    return existing_item


@app.delete("/items/{item_id}/", response_model=dict)
async def delete_item(item_id: int):
    item = await get_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await sync_to_async(item.delete)()
    return {"detail": "Item deleted"}


@app.get("/hello/")
async def read_root():
    return {"message": "Hello from FastAPI!"}
