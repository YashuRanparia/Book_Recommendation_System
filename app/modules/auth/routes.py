from fastapi import APIRouter, Depends, status, Form
from app.dependencies import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from app.modules.auth.schemas import UserSignup, UserLogin
from app.modules.auth import services as auth_services
from app.core.schemas import ResponseSchema

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=ResponseSchema)
def user_signup(session: Annotated[Session, Depends(get_db)], user_data: Annotated[UserSignup, Form()]):
    auth_services.user_signup(session, user_data)

    return {"status": "success", "message": "User created successfully!"}

@router.post("/login", status_code=status.HTTP_200_OK)
def user_login(session: Annotated[Session, Depends(get_db)], credentials: Annotated[UserLogin, Form()]):
    auth_services.user_login(session, credentials)