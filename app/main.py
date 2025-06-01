from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import logger
from app.modules.auth import routes as auth_routes

app = FastAPI(title='Book Recommendation System')

app.include_router(auth_routes.router)

@app.get('/')
def health_check():
    return 'Server is running ...'