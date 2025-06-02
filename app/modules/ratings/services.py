from sqlalchemy.orm import Session
from app.modules.ratings.schemas import RatingBase
from app.modules.auth.schemas import AuthenticatedUser
from app.modules.ratings import repository as rating_repo

def get_rating(session: Session, user: AuthenticatedUser, book_id: str):
    """Fetch a rating for a specific book by a user."""
    return rating_repo.get_rating(session, user.id, book_id)

def add_rating(session: Session, user: AuthenticatedUser, book_id: str, rating_data: RatingBase):
    rating_repo.add_rating(session, user.id, book_id, rating_data.model_dump())
    return {"status": "success","message": "Rating added successfully"}                            