from sqlalchemy.orm import Session
from app.modules.books.schemas import BookCreate, BookData
from app.modules.books import repository as book_repository
from app.modules.books.exceptions import BookNotFoundError, BookAlreadyExistsError
from fastapi import HTTPException, status

def create_book(session: Session, book_data: BookCreate):
    try:
        book_repository.create_book(session, book_data.model_dump(exclude_unset=True))
    except BookAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return {"status": "success", "message": "Book added successfully!"}

def get_book(session: Session, book_id: str) -> BookData:
    """
    Retrieve a book by its ID.
    
    Args:
        session: SQLAlchemy session for database operations.
        book_id: The ID of the book to retrieve.
    
    Returns:
        The book object if found, otherwise raises an HTTP 404 error.
    """
    try:
        return BookData.model_validate(book_repository.get_book(session, book_id), from_attributes=True)
    except BookNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e

def update_book(session: Session, book_id: str, book_data: BookCreate):
    """
    Update an existing book in the database.
    
    Args:
        session: SQLAlchemy session for database operations.
        book_id: The ID of the book to update.
        book_data: The updated data of the book.
    
    Returns:
        The updated book object.
    """
    try:
        return BookData.model_validate(book_repository.update_book(session, book_id, book_data.model_dump(exclude_unset=True)), from_attributes=True)
    except BookNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e

def delete_book(session: Session, book_id: str):
    """
    Delete a book by its ID.
    
    Args:
        session: SQLAlchemy session for database operations.
        book_id: The ID of the book to delete.
    
    Returns:
        None
    """
    try:
        book_repository.delete_book(session, book_id)
    except BookNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
    
def get_all_books(session: Session) -> list[BookData]:
    """
    Retrieve all books from the database.
    
    Args:
        session: SQLAlchemy session for database operations.
    
    Returns:
        A list of all book objects.
    """
    books = book_repository.get_all_books(session)
    return [BookData.model_validate(book, from_attributes=True) for book in books]

def search_book(session: Session, title: str):
    pass