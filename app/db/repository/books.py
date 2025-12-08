from sqlalchemy import select, func
from app.db import AsyncSessionLocal
from app.db.models.books import Book, Author, Genre, BookDetail, book_genre_table

class BookRepository:

    @staticmethod
    async def is_tables_empty() -> bool:
        async with AsyncSessionLocal() as session:
            count = await session.scalar(select(func.count()).select_from(Book))
            return count == 0

    @staticmethod
    async def list_books() -> list[Book]:
        async with AsyncSessionLocal() as session:
            result = await session.scalars(select(Book))
            return result.unique().all()

    @staticmethod
    async def create_book(data) -> Book:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                book = Book(
                    title=data.title,
                    author_id=data.author_id,
                    year_published=data.year_published,
                )
                session.add(book)
                await session.flush()

                # add genres
                if data.genre_ids:
                    for gid in data.genre_ids:
                        genre = await session.get(Genre, gid)
                        if genre:
                            book.genres.append(genre)

            return book

    @staticmethod
    async def delete_book(book_id: int) -> bool:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                book = await session.get(Book, book_id)
                if not book:
                    return False
                book.is_deleted = True
            return True
