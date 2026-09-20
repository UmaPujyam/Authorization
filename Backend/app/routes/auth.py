from fastapi import APIRouter, status

from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
)

from app.services.auth_service import (
    register_user,
    login_user,
    refresh_access_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED
)
def register(data: RegisterRequest):

    return register_user(data)


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(data: LoginRequest):

    return login_user(data)


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse
)
def refresh_token(data: RefreshTokenRequest):

    return refresh_access_token(data)