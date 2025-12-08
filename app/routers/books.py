from fastapi import APIRouter, HTTPException
from typing import List
from app.db.models.books import BookCreate, BookRead
from app.db.repository.books import BookRepository

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookRead])
async def read_books():
    return await BookRepository.list_books()


# @router.get("/books/", response_model=List[BookRead])
# async def read_books(session: AsyncSession):
#     result = await session.execute(select(Book))
#     books = result.scalars().all()
#     return [book_to_read(b) for b in books]  # конвертация в Pydantic

@router.post("/", response_model=BookRead)
async def add_book(data: BookCreate):
    return await BookRepository.create_book(data)

@router.delete("/{book_id}")
async def delete_book(book_id: int):
    ok = await BookRepository.delete_book(book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book marked as deleted"}
