from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.initial_data import (
    init_db,
    load_people_from_json,
    load_books_from_json,
)
from app.db.repository import PersonRepository, BookRepository
from app.routers import people, books


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ----------------------
    #        STARTUP
    # ----------------------
    await init_db()

    # --- Загрузка людей ---
    if await PersonRepository.is_table_empty():
        await load_people_from_json("people.json")

    # --- Загрузка книг ---
    if await BookRepository.is_table_empty():
        await load_books_from_json("books.json")

    yield

    # ----------------------
    #       SHUTDOWN
    # ----------------------
    # Здесь можно освободить ресурсы


app = FastAPI(
    title="People + Books API v2",
    lifespan=lifespan,
)

# Роутеры
app.include_router(people.router)
app.include_router(books.router)
