import json
from app.db import engine
from app.db.models import Person
from app.db.repository import PersonRepository
from app.db import Base

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def load_people_from_json(json_file: str):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        await PersonRepository.create_person(
            name=item["name"],
            age=item.get("age"),
            email=item.get("email")
        )
