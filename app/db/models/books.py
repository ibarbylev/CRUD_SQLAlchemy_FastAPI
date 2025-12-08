# app/db/models/books.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Text
from pydantic import BaseModel
from app.db import Base


# =============================
#   ORM МОДЕЛИ
# =============================

# ---------- Автор ----------
class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # связь many-to-many с книгами
    books: Mapped[list["Book"]] = relationship(
        back_populates="authors",
        secondary="book_authors"
    )


# ---------- Жанр ----------
class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    books: Mapped[list["Book"]] = relationship(
        back_populates="genres",
        secondary="book_genres"
    )


# ---------- Книга ----------
class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)

    # many-to-many
    authors: Mapped[list["Author"]] = relationship(
        back_populates="books",
        secondary="book_authors"
    )
    genres: Mapped[list["Genre"]] = relationship(
        back_populates="books",
        secondary="book_genres"
    )

    # one-to-one
    detail: Mapped["BookDetail"] = relationship(
        back_populates="book",
        uselist=False,
        cascade="all, delete-orphan"
    )


# ---------- Детализация книги (One-to-One) ----------
class BookDetail(Base):
    __tablename__ = "book_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        unique=True,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(Text)
    year: Mapped[int | None] = mapped_column(Integer)
    isbn: Mapped[str | None] = mapped_column(String, unique=True)

    book: Mapped["Book"] = relationship(back_populates="detail")


# =============================
#   ORM-АСОЦИАЦИИ (ТОЖЕ ORM)
# =============================

# many-to-many: книги ↔ авторы
class BookAuthor(Base):
    __tablename__ = "book_authors"

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"), primary_key=True
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"), primary_key=True
    )


# many-to-many: книги ↔ жанры
class BookGenre(Base):
    __tablename__ = "book_genres"

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"), primary_key=True
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genres.id"), primary_key=True
    )


# =============================
#   Pydantic-схемы
# =============================

class BookDetailCreate(BaseModel):
    description: str | None = None
    year: int | None = None
    isbn: str | None = None


class BookDetailRead(BaseModel):
    id: int
    description: str | None
    year: int | None
    isbn: str | None


class BookCreate(BaseModel):
    title: str
    authors: list[str] | None = None
    genres: list[str] | None = None
    detail: BookDetailCreate | None = None


class BookRead(BaseModel):
    id: int
    title: str
    authors: list[str]
    genres: list[str]
    detail: BookDetailRead | None
