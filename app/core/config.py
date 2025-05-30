from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = 'Book Recommendation System'
    db_name:str
    db_user: str
    db_password: str
    
    class Config:
        env_file = '../../env/.env.dev'

settings = Settings()