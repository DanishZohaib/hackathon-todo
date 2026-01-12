from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt, JWTError
from typing import Optional
from ..database.connection import get_db
from ..models.user import UserCreate, UserLogin, UserPublic
from ..models.response import TokenResponse, UserResponse
from ..services.auth_service import AuthService
from ..config import settings


auth_router = APIRouter()
auth_scheme = HTTPBearer()
auth_service = AuthService()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: Session = Depends(get_db)
) -> UserPublic:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = auth_service.get_user_by_email(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@auth_router.post("/signup", response_model=UserResponse)
def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = auth_service.get_user_by_email(db, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create the user
    db_user = auth_service.create_user(db, user_create)

    # Return user response
    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
        is_active=db_user.is_active
    )


@auth_router.post("/signin", response_model=TokenResponse)
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return TokenResponse(token=access_token, token_type="bearer")


@auth_router.post("/signout")
def logout_user():
    # In a real implementation, you might want to invalidate the token
    # For now, we'll just return a success message
    return {"message": "Successfully signed out"}