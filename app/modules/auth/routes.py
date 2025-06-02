from fastapi import APIRouter, Depends, status, Form
from app.dependencies import get_db, is_super_user
from typing import Annotated
from sqlalchemy.orm import Session
from app.modules.auth.schemas import UserSignup, UserLogin, SuperUserCreate, UserLoginDocs
from app.modules.auth import services as auth_services
from app.core.schemas import ResponseSchema

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=ResponseSchema)
def user_signup(session: Annotated[Session, Depends(get_db)], user_data: Annotated[UserSignup, Form()]):
    auth_services.user_signup(session, user_data)

    return {"status": "success", "message": "User created successfully!"}

@router.post("/login", status_code=status.HTTP_200_OK)
def user_login(session: Annotated[Session, Depends(get_db)], credentials: Annotated[UserLoginDocs, Form()]):
    auth_services.user_login(session, UserLogin(email=credentials.username, password=credentials.password.get_secret_value(), scopes=credentials.scope))

@router.post('/create_super_user', status_code=status.HTTP_201_CREATED, summary="Create a superuser", dependencies=[Depends(is_super_user)])
def create_super_user(session: Annotated[Session, Depends(get_db)], user_data: Annotated[SuperUserCreate, Form()], ):
    """
    Create a superuser.
    
    Args:
        session: SQLAlchemy session for database operations.
    
    Returns:
        None
    """
    auth_services.create_super_user(session, user_data)