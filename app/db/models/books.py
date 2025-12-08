# app/db/models/books.py
from typing import TYPE_CHECKING
from sqlalchemy import Table, Column, ForeignKey, Text, Boolean, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db import Base

# вспомогательная many-to-many table
book_genre_table = Table(
    "book_genre",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    books: Mapped[list["Book"]] = relationship(
        back_populates="author", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self):
        return f"<Author(name={self.name})>"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    year_published: Mapped[int] = mapped_column(Integer)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    author: Mapped["Author"] = relationship(back_populates="books", lazy="joined")
    detail: Mapped["BookDetail"] = relationship(
        back_populates="book", uselist=False, cascade="all, delete-orphan", lazy="selectin"
    )
    genres: Mapped[list["Genre"]] = relationship(
        secondary=book_genre_table, back_populates="books", lazy="selectin"
    )

    def __repr__(self):
        return f"<Book(title={self.title})>"


class BookDetail(Base):
    __tablename__ = "book_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False, unique=True)
    summary: Mapped[str] = mapped_column(Text)
    page_count: Mapped[int] = mapped_column(Integer)

    book: Mapped["Book"] = relationship(back_populates="detail", lazy="joined")

    def __repr__(self):
        return f"<BookDetail(book_id={self.book_id})>"


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    books: Mapped[list["Book"]] = relationship(
        secondary=book_genre_table, back_populates="genres", lazy="selectin"
    )

    def __repr__(self):
        return f"<Genre(name={self.name})>"