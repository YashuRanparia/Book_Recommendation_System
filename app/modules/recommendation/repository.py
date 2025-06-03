from sqlalchemy.orm import Session
from sqlalchemy import select, func as sqlfunc
from app.modules.books.models import Book
from app.modules.ratings.models import Rating

def get_top_n_rated_items(session: Session, items: int):
    '''
        Function to find top n items from DB based on ratings.
        Args:
            session: A sqlalchemy.orm.Session object
            items: int, Number of top items to recommend 
    '''
    try:
        stmt = select(Book, sqlfunc.avg(Rating.value).label("avg_rating")).join_from(Book, Rating, Book.id == Rating.book_id).group_by(Book.id, Rating.book_id)
        subq = stmt.subquery()
        
        ordered_result = select(subq).order_by(subq.c.avg_rating.desc())

        result = session.execute(ordered_result)

        columns = list(result._metadata.keys)

        fetched_values = list(result.fetchmany(items))

        response = []
        for rank, r in enumerate(fetched_values):
                book = Book(**{c: r[i] for i, c in enumerate(columns) if i < len(columns)-1})
                response.append({"rank":rank+1, "item": book, "rating": r[-1]})
        
        return response
    except Exception as e:
         raise e