from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt, JWTError
from typing import Optional
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from ..database.connection import get_session
from ..models.user import UserCreate, UserLogin, UserPublic
from ..models.response import TokenResponse, UserResponse, ForgotPasswordResponse, ResetPasswordResponse
from ..services.auth_service import AuthService
from ..config import settings

# Initialize rate limiter for this router
limiter = Limiter(key_func=get_remote_address)


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserPublic


class RegisterResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserPublic


auth_router = APIRouter()
auth_scheme = HTTPBearer()
auth_service = AuthService()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: Session = Depends(get_session)
) -> UserPublic:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_type = payload.get("token_type", "access")

        # Only allow access tokens for getting current user, not refresh tokens
        if token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token required for this operation",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Check if token has expired
        import time
        exp = payload.get("exp")
        if exp and exp < time.time():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = auth_service.get_user_by_email(db, user_email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@limiter.limit("10/hour")  # Limit signup attempts to 10 per hour per IP
@auth_router.post("/signup", response_model=RegisterResponse)
def register_user(request: Request, user_create: UserCreate, db: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = auth_service.get_user_by_email(db, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create the user
    db_user = auth_service.create_user(db, user_create)

    # Create access and refresh tokens for the new user
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    refresh_token = auth_service.create_refresh_token(
        data={"sub": db_user.email}
    )

    # Return user response with tokens
    return RegisterResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserPublic(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            is_active=db_user.is_active
        )
    )


@limiter.limit("5/minute")  # Limit login attempts to 5 per minute per IP
@auth_router.post("/signin", response_model=LoginResponse)
def login_user(request: Request, user_login: UserLogin, db: Session = Depends(get_session)):
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
    refresh_token = auth_service.create_refresh_token(
        data={"sub": user.email}
    )

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserPublic(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active
        )
    )


@limiter.limit("10/minute")  # Limit token refresh attempts to 10 per minute per IP
@auth_router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: Request, credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """
    Refresh access token using refresh token
    The refresh token is passed in the Authorization header
    """
    refresh_token_str = credentials.credentials

    # Verify the refresh token
    user_id = auth_service.verify_refresh_token(refresh_token_str)

    # Create a new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )

    # Create a new refresh token (optional - rotate refresh tokens)
    new_refresh_token = auth_service.create_refresh_token(
        data={"sub": user_id}
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )


@auth_router.post("/signout")
def logout_user():
    # In a real implementation, you might want to invalidate the token
    # For now, we'll just return a success message
    return {"message": "Successfully signed out"}


@auth_router.get("/profile", response_model=UserResponse)
def get_profile(current_user: UserPublic = Depends(get_current_user)):
    """Get current user's profile information"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        is_active=current_user.is_active
    )


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


@limiter.limit("3/minute")  # Limit forgot password requests to 3 per minute per IP
@auth_router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(request: Request, forgot_request: ForgotPasswordRequest, db: Session = Depends(get_session)):
    """Generate password reset token and send email notification"""
    # Check if user exists
    user = auth_service.get_user_by_email(db, forgot_request.email)

    if user:  # Only send reset if user exists, but don't reveal if email exists
        # Create password reset token
        reset_token = auth_service.create_password_reset_token(forgot_request.email)

        # In a real application, you would send an email with the reset token
        # For now, we'll just return a generic message
        # Example: send_reset_email(request.email, reset_token)

        # Note: In production, send the reset token via email to the user
        # For security, don't reveal whether the email exists in the system
        pass

    # Always return the same message to avoid email enumeration
    return ForgotPasswordResponse(message="If an account exists with this email, a password reset link has been sent")


@limiter.limit("5/hour")  # Limit password reset attempts to 5 per hour per IP
@auth_router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(request: Request, reset_request: ResetPasswordRequest, db: Session = Depends(get_session)):
    """Reset user's password using the reset token"""
    # Verify the reset token and get the email
    email = auth_service.verify_password_reset_token(reset_request.token)

    # Reset the password (validation is handled inside the service method)
    success = auth_service.reset_password(db, email, reset_request.new_password)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return ResetPasswordResponse(message="Password reset successfully")