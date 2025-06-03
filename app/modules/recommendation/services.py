from sqlalchemy.orm import Session
from app.modules.recommendation.repository import get_top_n_rated_items
from app.modules.recommendation.schemas import RecommendedItem
from fastapi import HTTPException, status

def recommend_item(session: Session, items: int):
    try:
        result = get_top_n_rated_items(session, items)
        return [RecommendedItem(**i) for i in result]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching records")