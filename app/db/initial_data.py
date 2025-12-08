import json
from app.db import engine, Base
from app.db.repository.person import PersonRepository
from app.db.repository.books import BookRepository
from app.db.models.person import Person
from app.db.models.books import Author, Genre, Book, BookDetail, BookGenre
from sqlalchemy import insert
from app.db import AsyncSessionLocal
from sqlalchemy.schema import DropTable

# ---------------------------------------------------------
# INIT DB: DROP ALL → CREATE ALL
# ---------------------------------------------------------

from sqlalchemy import text

async def init_db():
    async with engine.begin() as conn:
        # удаляем таблицы с зависимостями через raw SQL
        await conn.execute(text("DROP TABLE IF EXISTS book_genres CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS book_details CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS books CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS authors CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS genres CASCADE"))
        # создаём все таблицы ORM
        await conn.run_sync(Base.metadata.create_all)



# ---------------------------------------------------------
# LOAD PEOPLE
# ---------------------------------------------------------
async def load_people_from_json(json_file: str):
    with open(json_file, "r", encoding="utf-8") as f:
        people = json.load(f)

    for item in people:
        await PersonRepository.create_person(
            name=item["name"],
            age=item.get("age"),
            email=item.get("email"),
        )


# ---------------------------------------------------------
# LOAD BOOKS (authors, genres, books, book_details)
# ---------------------------------------------------------
async def load_books_from_json(json_file: str):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    authors = data["authors"]
    genres = data["genres"]
    books = data["books"]
    details = data["book_details"]

    async with AsyncSessionLocal() as session:  # type: AsyncSession
        async with session.begin():

            # -------- AUTHORS --------
            for a in authors:
                session.add(Author(
                    id=a["id"],
                    name=a["name"]
                ))

            # -------- GENRES --------
            for g in genres:
                session.add(Genre(
                    id=g["id"],
                    name=g["name"]
                ))

            await session.flush()  # применяем вставки, чтобы id были доступны

            # -------- BOOKS --------
            for b in books:
                book = Book(
                    id=b["id"],
                    title=b["title"],
                    author_id=b["author_id"],
                    year_published=b.get("year_published"),
                    is_deleted=b.get("is_deleted", False)
                )
                session.add(book)
                await session.flush()

                # many-to-many genres
                book.genres = [
                    await session.get(Genre, gid) for gid in b.get("genre_ids", [])
                    if await session.get(Genre, gid) is not None
                ]

                session.add(book)

            await session.flush()

            # -------- BOOK DETAILS --------
            for d in details:
                book = await session.get(Book, d["book_id"])
                if book:
                    book.detail = BookDetail(
                        summary=d.get("summary"),
                        page_count=d.get("page_count")
                    )

# ---------------------------------------------------------
# Full initialization call (optional helper)
# ---------------------------------------------------------
async def init_all_data():
    await init_db()
    await load_people_from_json("people.json")
    await load_books_from_json("books.json")
