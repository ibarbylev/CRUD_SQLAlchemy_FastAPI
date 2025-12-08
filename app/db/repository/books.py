from sqlalchemy import select, func, text
from app.db import AsyncSessionLocal
from app.db.models.books import Book, Author, Genre, BookDetail, BookRead
from sqlalchemy.ext.asyncio import AsyncSession

class BookRepository:

    @staticmethod
    async def is_tables_empty() -> bool:
        async with AsyncSessionLocal() as session:
            count = await session.scalar(select(func.count()).select_from(Book))
            return count == 0

    @staticmethod
    async def list_books() -> list[dict]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Book))
            books = result.scalars().all()
            return [
                {
                    "id": b.id,
                    "title": b.title,
                    "author_id": b.author_id,
                    "year_published": b.year_published,
                    "is_deleted": b.is_deleted,
                    "genre_ids": [g.id for g in b.genres],
                    "detail": {
                        "id": b.detail.id if b.detail else None,
                        "summary": b.detail.summary if b.detail else None,
                        "page_count": b.detail.page_count if b.detail else None
                    }
                }
                for b in books
            ]

    # @staticmethod
    # async def create_book(data) -> Book:
    #     async with AsyncSessionLocal() as session:
    #         async with session.begin():
    #             book = Book(
    #                 title=data.title,
    #                 author_id=data.author_id,
    #                 year_published=data.year_published,
    #                 is_deleted=False  # можно по умолчанию False
    #             )
    #             session.add(book)
    #             await session.flush()  # чтобы book.id стал доступен
    #
    #             # add genres
    #             if data.genre_ids:
    #                 for gid in data.genre_ids:
    #                     genre = await session.get(Genre, gid)
    #                     if genre:
    #                         book.genres.append(genre)
    #         return book
    @staticmethod
    async def create_book(data) -> Book:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                # синхронизируем sequence автоматически
                await session.execute(
                    text("SELECT setval('books_id_seq', (SELECT MAX(id) FROM books))")
                )

                book = Book(
                    title=data.title,
                    author_id=data.author_id,
                    year_published=data.year_published,
                    is_deleted=False
                )
                session.add(book)
                await session.flush()

                # genres
                if data.genre_ids:
                    result = await session.execute(
                        select(Genre).where(Genre.id.in_(data.genre_ids))
                    )
                    book.genres = result.scalars().all()

                # details
                if data.detail:
                    book.detail = BookDetail(
                        summary=data.detail.summary,
                        page_count=data.detail.page_count
                    )
            return book

    @staticmethod
    async def delete_book(book_id: int) -> bool:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                book = await session.get(Book, book_id)
                if not book:
                    return False
                await session.delete(book)
            return True
