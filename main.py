from fastapi import FastAPI, HTTPException, status
from models.db import db
from models.models import Sheep
from typing import List

app = FastAPI()

@app.get("/sheep", response_model=List[Sheep])
def read_all_sheep():
    return list(db.data.values())

@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    sheep = db.get_sheep(id)
    if not sheep:
        raise HTTPException(status_code=404, detail="Sheep not found")
    return sheep

@app.post("/sheep", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    if sheep.id in db.data:
        raise HTTPException(status_code=400, detail="Sheep already exists")
    db.add_sheep(sheep)
    return sheep

@app.put("/sheep/{id}", response_model=Sheep)
def update_sheep(id: int, sheep: Sheep):
    if sheep.id != id:
        raise HTTPException(status_code=400, detail="ID mismatch")
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep not found")
    db.data[id] = sheep
    return sheep

@app.delete("/sheep/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sheep(id: int):
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep not found")
    del db.data[id]