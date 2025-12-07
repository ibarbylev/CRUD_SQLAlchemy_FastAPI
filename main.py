import asyncio
from load_data import load_people_from_json, init_db
from crud_person import (
    is_table_empty, get_people, create_person, update_person_email, delete_person
)

async def main():
    await init_db()

    if await is_table_empty():
        print("Таблица пуста. Загружаем people.json ...")
        await load_people_from_json("people.json")
    else:
        print("Таблица уже содержит данные.")

    print("\nСодержимое таблицы после загрузки:")
    people = await get_people()
    for p in people:
        print(f"{p.id}: {p.name}, {p.age}, {p.email}")

    # ---- Create ----
    print("\nДобавляем нового человека Dave ...")
    await create_person("Dave", 28, "dave@example.com")

    # ---- Update ----
    print("\nОбновляем email Alice ...")
    await update_person_email(1, "alice_new@example.com")

    # ---- Delete ----
    print("\nУдаляем Bob ...")
    await delete_person(2)

    # ---- Read после изменений ----
    print("\nСодержимое таблицы после изменений:")
    people = await get_people()
    for p in people:
        print(f"{p.id}: {p.name}, {p.age}, {p.email}")

if __name__ == "__main__":
    asyncio.run(main())
