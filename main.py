from enum import Enum
from typing import Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world!"}

@app.get("/name/{name}")
def get_name(name: str):
    return {"name": name}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW"}
    if model_name.value == ModelName.lenet:
        return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10, q:Optional[str] = Query(None, max_length=5)):
    results = fake_items_db[skip: skip + limit]
    if q:
        print(f"{q=}")
    return results


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.post("/items/")
async def create_item(item: Item):
    print(f"=> {item=}")
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": 1})
    return result

