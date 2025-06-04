from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.modules.books.models import Book
from app.modules.books.exceptions import BookNotFoundError, BookAlreadyExistsError
from datetime import datetime
from app.core.constants import tzinfo
from app.modules.ratings.models import Rating

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
    book = session.query(Book).filter(Book.title == book_data['title'], Book.author == book_data['author'], Book.deleted_at == None).first()
    if book:
        raise BookAlreadyExistsError(book_data['title'], book_data['author'])

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
    book = session.query(Book).filter(Book.id == book_id, Book.deleted_at == None).first()
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
        book.deleted_at = datetime.now(tzinfo)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    
def get_books(session: Session, *, title: str = None, author: str = None, rating: float = 0.0):
    """
    Retrieve all books from the database.
    
    Args:
        session: SQLAlchemy session for database operations.
    
    Returns:
        A list of all book objects.
    """

    # stmt = select(Book).filter(Book.deleted_at == None)
    stmt = select(Book, func.avg(Rating.value).label("avg_rating")).join_from(Book, Rating, Book.id == Rating.book_id).group_by(Book.id, Rating.book_id).having(Book.deleted_at == None, Book.title == title if title else True, Book.author == author if author else True)
    subq = stmt.subquery()
    filtered_data_q = select(subq).filter(subq.c.avg_rating >= rating)
    
    # ordered_result = select(subq).order_by(subq.c.avg_rating.desc())

    books = session.execute(filtered_data_q).fetchall()
    # print(books)
    return books

def get_book_based_on_title(session: Session, title: str):
    stmt = select(Book).filter(Book.title == title)
    book = session.execute(stmt).first()

    if not book:
        raise BookNotFoundError()

    return book