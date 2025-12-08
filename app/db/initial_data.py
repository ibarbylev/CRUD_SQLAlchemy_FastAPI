import json
from app.db import engine, Base
from app.db.repository.person import PersonRepository
from app.db.repository.books import BookRepository
from app.db.models.person import Person
from app.db.models.books import Author, Genre, Book, BookDetail
from sqlalchemy import insert
from app.db import AsyncSessionLocal


# ---------------------------------------------------------
# INIT DB: DROP ALL → CREATE ALL
# ---------------------------------------------------------
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
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

    async with AsyncSessionLocal() as session:
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

            await session.flush()

            # -------- BOOKS --------
            for b in books:
                book = Book(
                    id=b["id"],
                    title=b["title"],
                    author_id=b["author_id"],
                    year_published=b["year_published"],
                    is_deleted=b["is_deleted"],
                )
                session.add(book)
                await session.flush()

                # assign many-to-many genres
                for gid in b["genre_ids"]:
                    genre = await session.get(Genre, gid)
                    if genre:
                        book.genres.append(genre)

            await session.flush()

            # -------- BOOK DETAILS --------
            for d in details:
                session.add(BookDetail(
                    book_id=d["book_id"],
                    summary=d["summary"],
                    page_count=d["page_count"]
                ))


# ---------------------------------------------------------
# Full initialization call (optional helper)
# ---------------------------------------------------------
async def init_all_data():
    await init_db()
    await load_people_from_json("people.json")
    await load_books_from_json("books.json")
