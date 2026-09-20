from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.shared.security import hash_password, verify_password

from app.shared.token import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)


user_repository = UserRepository()


def register_user(data):

    if user_repository.get_by_email(data.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = hash_password(data.password)

    try:
        user = user_repository.create(
            data.name,
            data.email,
            hashed_password
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to register user",
        )

    return {
        "message": "User registered successfully",
        "user_id": user.user_id,
    }


def login_user(data):

    try:
        user = user_repository.get_by_email(data.email)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service unavailable",
        )

    if user is None or not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user.user_id)

    refresh_token = create_refresh_token(user.user_id)

    return {
        "message": "Login successful",
        "user_id": user.user_id,
        "name": user.name,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def refresh_access_token(data):

    payload = verify_refresh_token(
        data.refresh_token
    )

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    try:
        user_id = int(payload["user_id"])

    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    try:
        user = user_repository.get_by_id(user_id)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service unavailable",
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is no longer available",
        )

    new_access_token = create_access_token(
        user.user_id
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }