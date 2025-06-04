from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from app.modules.ratings.models import Rating

def get_avg_rating():
    stmt = select(Rating.book_id, func.avg(Rating.value).label("avg_rating")).group_by(Rating.book_id).subquery()
    return stmt