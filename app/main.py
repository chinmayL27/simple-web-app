from contextlib import asynccontextmanager
import os
import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

DATABASE_PATH = Path(os.getenv("DATABASE_PATH", "data/app.db"))


def connect_database() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


@asynccontextmanager
async def lifespan(_: FastAPI):
    with connect_database() as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT ''
            )"""
        )
    yield


app = FastAPI(title="Interview Practice API", lifespan=lifespan)


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)


class Item(BaseModel):
    id: int
    name: str
    description: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemCreate):
    with connect_database() as connection:
        cursor = connection.execute(
            "INSERT INTO items (name, description) VALUES (?, ?)",
            (item.name, item.description),
        )
        row = connection.execute(
            "SELECT id, name, description FROM items WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return dict(row)


@app.get("/items", response_model=list[Item])
def list_items():
    with connect_database() as connection:
        rows = connection.execute(
            "SELECT id, name, description FROM items ORDER BY id"
        ).fetchall()
    return [dict(row) for row in rows]


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    with connect_database() as connection:
        row = connection.execute(
            "SELECT id, name, description FROM items WHERE id = ?", (item_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(row)
