from sqlalchemy.orm import Session
from app.modules.auth.schemas import UserSignup, UserLogin, Token, PayloadSchema
from app.modules.users import repository as user_repo
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_password, create_jwt_token
from app.core.logging import logger
from app.modules.users.exceptions import UserAlreadyExistsException

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    # scopes={"user-r": "Read permission for user.", 'user-w': "Write permission for user."}
    )  

def user_signup(session: Session, user_data: UserSignup):
    """
    Function to handle user signup.
    This function will contain the logic for signing up a user.
    """
    try: 
        user_repo.user_create(session, user_data.model_dump(exclude_unset=True))
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def user_login(session: Session, credentials: UserLogin):
    """
    Function to handle user login.
    This function will contain the logic for logging in a user.
    """
    user = user_repo.get_user(session, email=credentials.email)
    payload = PayloadSchema(id=user.id)
    if verify_password(credentials.password, user.password):
        access_token = create_jwt_token(payload)
        return Token(access_token=access_token, token_type='bearer')
    logger.info('password not verified')
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )