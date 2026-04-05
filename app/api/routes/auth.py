from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.schemas.requests.auth_requests import LoginRequest, SignupRequest
from app.api.schemas.responses.auth_responses import LoginResponse, RefreshTokenResponse
from app.api.schemas.responses.common_responses import FailResponse, SuccessResponse
from app.config import settings
from app.db.database import get_db
from app.services.auth.login_service import LoginService
from app.services.auth.logout_service import LogoutService
from app.services.auth.refresh_token_service import RefreshTokenService
from app.services.auth.signup_service import SignupService
from app.services.schemas.auth_schemas import LoginData, SignupData
from app.util.tokens import REFRESH_KEY, get_refresh_token_id


router = APIRouter()


@router.post('/signup',
             response_model=SuccessResponse,
             responses={
                 400: {'model': FailResponse},
                 500: {'model': FailResponse},
             },
             status_code=status.HTTP_201_CREATED)
def signup(
    *,
    session: Session = Depends(get_db),
    body: SignupRequest,
):
    SignupService(session).signup(SignupData(**body.model_dump()))
    return SuccessResponse(code=status.HTTP_201_CREATED)


@router.post('/login',
             response_model=SuccessResponse[LoginResponse],
             responses={
                 400: {'model': FailResponse},
                 401: {'model': FailResponse},
                 500: {'model': FailResponse},
             },
             status_code=status.HTTP_200_OK)
def login(
    *,
    session: Session = Depends(get_db),
    body: LoginRequest,
):
    auth_token, refresh_token = LoginService(session).login(LoginData(**body.model_dump()))
    response = JSONResponse(
        content=SuccessResponse(data={'token': auth_token}).model_dump(),
    )
    response.set_cookie(
        key=REFRESH_KEY,
        value=refresh_token,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        httponly=True,
        secure=not settings.debug_mode,
        samesite='lax',
    )
    return response


@router.post('/refresh',
             response_model=SuccessResponse[RefreshTokenResponse],
             responses={
                 400: {'model': FailResponse},
                 500: {'model': FailResponse},
             },
             status_code=status.HTTP_200_OK)
def refresh_token(
    *,
    session: Session = Depends(get_db),
    request: Request,
):
    refresh_cookie = request.cookies.get(REFRESH_KEY)
    refresh_token_id = get_refresh_token_id(refresh_cookie)
    new_token = RefreshTokenService(session).refresh_auth_jwt(refresh_token_id)
    return SuccessResponse(data={'token': new_token})


@router.post('/logout',
             response_model=SuccessResponse,
             status_code=status.HTTP_200_OK)
def logout(
    *,
    session: Session = Depends(get_db),
    request: Request,
):
    refresh_cookie = request.cookies.get(REFRESH_KEY)
    refresh_token_id = get_refresh_token_id(refresh_cookie)
    LogoutService(session).logout(refresh_token_id)
    response = JSONResponse(content=SuccessResponse().model_dump())
    response.delete_cookie(REFRESH_KEY)
    return response
