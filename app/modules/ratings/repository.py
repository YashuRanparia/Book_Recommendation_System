from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from app.modules.ratings.models import Rating
from app.modules.ratings.exceptions import RatingNotFoundException

def get_rating(session: Session, user_id: str, book_id: str) -> Rating:
    """Fetch a rating for a specific book by a user."""
    rating = session.query(Rating).filter_by(book_id=book_id, user_id=user_id).first()

    if not rating:
        raise RatingNotFoundException(f'Rating not found for book_id: {book_id} and user_id: {user_id}')
    
    return rating

def add_rating(session: Session, user_id: str, book_id: str, rating_data: dict):
    rating = session.query(Rating).filter_by(book_id=book_id, user_id=user_id).first()
    
    try:
        if rating:
            rating.value = rating_data['value']
        else:
            rating = Rating(book_id=book_id, user_id=user_id, value=rating_data['value'])
            session.add(rating)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f'IntegrityError: {e.orig}') 