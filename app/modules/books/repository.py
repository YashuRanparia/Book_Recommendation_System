from sqlalchemy.orm import Session
from app.modules.books.models import Book
from app.modules.books.exceptions import BookNotFoundError

def create_book(session: Session, book_data: dict):
    """
    Create a new book in the database.
    
    Args:
        session: SQLAlchemy session for database operations.
        book_data: Data for the book to be created.
    
    Returns:
        The created book object.
    """
    # Assuming `Book` is a SQLAlchemy model and `book_data` is a python dictionary
    new_book = Book(**book_data)
    try:
        session.add(new_book)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    
def get_book(session: Session, book_id: str):
    """
    Retrieve a book by its ID.
    
    Args:
        session: SQLAlchemy session for database operations.
        book_id: The ID of the book to retrieve.
    
    Returns:
        The book object if found, otherwise raises an HTTP 404 error.
    """
    book = session.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise BookNotFoundError(book_id)
    return book

def update_book(session: Session, book_id: str, book_data: dict):
    """
    Update an existing book in the database.
    
    Args:
        session: SQLAlchemy session for database operations.
        book_id: The ID of the book to update.
        book_data: The updated data of the book.
    
    Returns:
        The updated book object.
    """
    book = get_book(session, book_id)
    for key, value in book_data.items():
        setattr(book, key, value)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    return book

def delete_book(session: Session, book_id: str):
    """
    Delete a book by its ID.
    
    Args:
        session: SQLAlchemy session for database operations.
        book_id: The ID of the book to delete.
    
    Returns:
        None
    """
    book = get_book(session, book_id)
    try:
        session.delete(book)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e