from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.initial_data import init_db, load_people_from_json
from app.db.repository import PersonRepository
from app.routers import people


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    await init_db()
    if await PersonRepository.is_table_empty():
        await load_people_from_json("people.json")
    yield
    # --- SHUTDOWN ---
    # Здесь можно добавить код для завершения работы, если нужно
    # например: await some_cleanup()


app = FastAPI(title="People API v2", lifespan=lifespan)

# Подключаем роутеры
app.include_router(people.router)
