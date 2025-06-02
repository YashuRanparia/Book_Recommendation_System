from fastapi import FastAPI
from pydantic_settings import BaseSettings
from zoneinfo import ZoneInfo

class Settings(BaseSettings):
    app_name: str = 'Book Recommendation System'
    stage: str = 'DEVELOPMENT'
    debug: bool = True

    # Database Configuration
    db_scheme: str
    db_name:str
    db_user: str
    db_password: str
    db_port: int
    db_host: str
    log_level:int = 20

    secret_key: str
    jwt_hashing_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30

    tz: str = 'Asia/Kolkata'
    
    class Config:
        env_file = 'env/.env.dev'

settings = Settings()