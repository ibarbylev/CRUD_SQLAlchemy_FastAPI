import asyncio
import json
from database import engine, AsyncSessionLocal, Base
from models_person import Person


async def init_db():
    async with engine.begin() as conn:
        # На время разработки: очищаем и создаём таблицы
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def load_people_from_json(json_file: str):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    async with AsyncSessionLocal() as session:
        async with session.begin():
            for item in data:
                person = Person(
                    name=item["name"],
                    age=item.get("age"),
                    email=item.get("email")
                )
                session.add(person)

        await session.commit()


async def main():
    await init_db()
    await load_people_from_json("people.json")


if __name__ == "__main__":
    asyncio.run(main())
