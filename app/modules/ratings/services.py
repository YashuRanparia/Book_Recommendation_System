from sqlalchemy.orm import Session
from app.modules.ratings.schemas import RatingBase
from app.modules.auth.schemas import AuthenticatedUser
from app.modules.ratings import repository as rating_repo

def create_rating(session: Session, user: AuthenticatedUser, book_id: str, rating_data: RatingBase):
    return rating_repo.create_rating(session, user.id, rating_data.model_dump())                            