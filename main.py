import databases
import sqlalchemy
from fastapi import FastAPI, Request

from decouple import config


DATABASE_URL = f"postgresql://" \
               f"{config('DB_USER')}:" \
               f"{config('DB_PASSWORD')}@" \
               f"{config('DB_SERVER')}:" \
               f"{config('DB_PORT')}/" \
               f"{config('DB_DATABASE')}"

data = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("author", sqlalchemy.String),
    sqlalchemy.Column("pages", sqlalchemy.Integer)
)

readers = sqlalchemy.Table(
    "readers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String)
)

readers_books = sqlalchemy.Table(
    "readers_books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("book_id", sqlalchemy.ForeignKey("books.id"), nullable=False),
    sqlalchemy.Column("header_id", sqlalchemy.ForeignKey("readers.id"), nullable=False),
)

app = FastAPI()


@app.get("/startup")
async def startup():
    await data.connect()


@app.get("/shutdown")
async def shutdown():
    await data.disconnect()


@app.get("/books/")
async def get_all_books():
    query = books.select()
    return await data.fetch_all(query)


@app.post("/books/")
async def create_books(request: Request):
    datas = await request.json()
    query = books.insert().values(**datas)
    last_record_id = await data.execute(query)
    return {"id": last_record_id}


