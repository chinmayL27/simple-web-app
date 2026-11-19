from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# SQLite stores the database in a local file created automatically.
DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False, default="")


Base.metadata.create_all(bind=engine)


class RecordCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str = ""


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/records", status_code=201)
def create_record(record: RecordCreate, db: Session = Depends(get_db)):
    new_record = Record(name=record.name, description=record.description)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@app.get("/records")
def list_records(db: Session = Depends(get_db)):
    return db.query(Record).all()


@app.get("/records/{record_id}")
def get_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(Record).filter(Record.id == record_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record
