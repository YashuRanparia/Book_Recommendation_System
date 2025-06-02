from fastapi import APIRouter, Depends, status, Form, Path, Security
from sqlalchemy.orm import Session
from app.dependencies import get_db
from typing import Annotated
from app.modules.books.schemas import BookCreate, BookData
from app.modules.books import services as book_services
from app.dependencies import is_super_user, get_authenticated_user
from app.modules.auth.schemas import AuthenticatedUser
from app.core.schemas import ResponseSchema

router = APIRouter(prefix="/books", tags=["books"]) 

@router.post("/create", summary="Create a new book", status_code=status.HTTP_201_CREATED, dependencies=[Depends(is_super_user)], response_model=ResponseSchema)
def create_book(session: Annotated[Session, Depends(get_db)], book_data: Annotated[BookCreate, Form()]):
    """
    Create a new book in the database.
    Args:
        session: SQLAlchemy session for database operations.
        book_data: The data of the book to be created.
    Returns:
        None
    """
    return book_services.create_book(session, book_data)

@router.get("/get/{book_id}", summary="Get a book by ID", response_model=BookData, status_code=status.HTTP_200_OK)
def get_book(session: Annotated[Session, Depends(get_db)], book_id: Annotated[str, Path(description="The ID of the book to retrieve")], user: Annotated[AuthenticatedUser, Security(get_authenticated_user, scopes=['user-r'])]):
    """
    Retrieve a book by its ID.
    
    Args:
        session: SQLAlchemy session for database operations.
        book_id: The ID of the book to retrieve.
    
    Returns:
        The book object if found, otherwise raises an HTTP 404 error.
    """
    return book_services.get_book(session, book_id)

@router.patch('/update/{book_id}', summary="Update an existing book", status_code=status.HTTP_200_OK, dependencies=[Depends(is_super_user)], response_model=BookData)
def update_book(session: Annotated[Session, Depends(get_db)], book_id: Annotated[str, Path(description="The ID of the book to update")], book_data: Annotated[BookCreate, Form()]):
    """
    Update an existing book in the database.
    
    Args:
        session: SQLAlchemy session for database operations.
        book_id: The ID of the book to update.
        book_data: The updated data of the book.
    
    Returns:
        None
    """
    return book_services.update_book(session, book_id, book_data)

@router.delete('/delete/{book_id}', summary="Delete a book by ID", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_super_user)])
def delete_book(session: Annotated[Session, Depends(get_db)], book_id: Annotated[str, Path(description="The ID of the book to delete")]):
    """
    Delete a book by its ID.
    
    Args:
        session: SQLAlchemy session for database operations.
        book_id: The ID of the book to delete.
    
    Returns:
        None
    """
    book_services.delete_book(session, book_id)


@router.get("/get-all", summary="Get all books", response_model=list[BookData], status_code=status.HTTP_200_OK)
def get_all_books(session: Annotated[Session, Depends(get_db)], user: Annotated[AuthenticatedUser, Security(get_authenticated_user, scopes=['user-r'])]):
    """
    Retrieve all books from the database.
    
    Args:
        session: SQLAlchemy session for database operations.
    
    Returns:
        A list of all books.
    """
    return book_services.get_all_books(session)