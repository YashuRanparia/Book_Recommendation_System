from app.core.db import DBConnection

def get_db():
    """
    Dependency to get a database connection.
    This function can be used in FastAPI routes to ensure a database connection is available.
    """
    db = DBConnection()
    session = db.create_session()
    try:
        yield session
    finally:
        session.close()