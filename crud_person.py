from sqlalchemy import select, func
from database import AsyncSessionLocal
from models_person import Person

# ----------- CRUD функции -------------

async def is_table_empty() -> bool:
    async with AsyncSessionLocal() as session:
        count = await session.scalar(select(func.count()).select_from(Person))
        return count == 0

async def get_people():
    async with AsyncSessionLocal() as session:
        result = await session.scalars(select(Person))
        return result.all()

async def create_person(name: str, age: int, email: str):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            person = Person(name=name, age=age, email=email)
            session.add(person)
        await session.commit()
        return person

async def update_person_email(person_id: int, new_email: str):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Получаем объект из базы
            person = await session.get(Person, person_id)
            if person:
                person.email = new_email
                # session.commit() не нужен внутри begin(), он выполнится после выхода
        # После выхода из блока begin() изменения автоматически зафиксируются

async def delete_person(person_id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            person = await session.get(Person, person_id)
            if person:
                await session.delete(person)
        # После выхода из блока begin() удаление будет зафиксировано

