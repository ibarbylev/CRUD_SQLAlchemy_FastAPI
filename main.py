import asyncio
from sqlalchemy import select, func

from database import AsyncSessionLocal
from models_person import Person
from load_data import load_people_from_json, init_db

# ------------ устаревший синтаксис ---------------

# async def is_table_empty() -> bool:
#     async with AsyncSessionLocal() as session:
#         result = await session.execute(select(func.count()).select_from(Person))
#         count = result.scalar()
#         return count == 0


# async def get_people():
#     async with AsyncSessionLocal() as session:
#         result = await session.execute(select(Person))
#         return result.scalars().all()

# ------------ новый синтаксис ---------------

async def is_table_empty() -> bool:
    async with AsyncSessionLocal() as session:
        count = await session.scalar(
            select(func.count()).select_from(Person)
        )
        return count == 0


async def get_people():
    async with AsyncSessionLocal() as session:
        return await session.scalars(select(Person))


async def main():
    await init_db()

    if await is_table_empty():
        print("Таблица пуста. Загружаем people.json ...")
        await load_people_from_json("people.json")
    else:
        print("Таблица уже содержит данные.")

    people = await get_people()

    print("\nСодержимое таблицы people:")
    for p in people:
        print(f"{p.id}: {p.name}, {p.age}, {p.email}")


if __name__ == "__main__":
    asyncio.run(main())
