from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.modules.ratings.models import Rating

def create_rating(session: Session, user_id: str, book_id: str, rating_data: dict):
    rating = Rating(book_id=book_id, user_id=user_id, value=rating_data['value'])
    
    try:
        session.add(rating)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f'IntegrityError: {e.orig}')