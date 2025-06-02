from fastapi import APIRouter, Depends, Path, Form
from app.dependencies import get_db ,get_authenticated_user
from app.modules.auth.schemas import AuthenticatedUser
from app.modules.ratings.schemas import RatingBase
from sqlalchemy.orm import Session
from typing import Annotated
from app.modules.ratings import services as rating_service

router = APIRouter(prefix="/rating", tags=["Rating"])

@router.post('/create', description="Add ratings for the item")
def create_rating(session: Annotated[Session, Depends(get_db)], user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)], book_id: Annotated[str, Path()], rating_data: Annotated[RatingBase, Form()]):
    return rating_service.create_rating(session, user, book_id, rating_data)