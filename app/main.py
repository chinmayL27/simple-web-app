from contextlib import asynccontextmanager
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, insert, select, text
from sqlalchemy.engine import Engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
metadata = MetaData()
records_table = Table(
    "records", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("description", String(500), nullable=False, server_default=""),
)
engine: Engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    if DATABASE_URL.startswith("sqlite"):
        os.makedirs("data", exist_ok=True)
    metadata.create_all(engine)
    yield
    engine.dispose()


app = FastAPI(title="Application API", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


class RecordCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)


class Record(BaseModel):
    id: int
    name: str
    description: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/records", response_model=Record, status_code=201)
def create_record(record: RecordCreate):
    with engine.begin() as connection:
        result = connection.execute(
            insert(records_table).values(name=record.name, description=record.description)
        )
        row = connection.execute(
            select(records_table).where(records_table.c.id == result.inserted_primary_key[0])
        ).mappings().one()
    return dict(row)


@app.get("/records", response_model=list[Record])
def list_records():
    with engine.connect() as connection:
        rows = connection.execute(select(records_table).order_by(records_table.c.id)).mappings().all()
    return [dict(row) for row in rows]


@app.get("/records/{record_id}", response_model=Record)
def get_record(record_id: int):
    with engine.connect() as connection:
        row = connection.execute(
            select(records_table).where(records_table.c.id == record_id)
        ).mappings().first()
    if row is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return dict(row)
