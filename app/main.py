from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes.router import router
from app.api.schemas.responses.common_responses import FailResponse
from app.config import settings
from app.db.database import init_db
from app.util.errors import CustomError, UnauthorizedError
from app.util.tokens import REFRESH_KEY


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    debug=settings.debug_mode,
    lifespan=lifespan,
)


app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, e: RequestValidationError):
    print('validation exception handler ')
    messages = [f'{error['loc'][-1]} {error['msg']}' for error in e.errors()]
    message = '\n'.join(messages)
    return JSONResponse(
        content=FailResponse(
            errors='Invalid request.',
            code=status.HTTP_400_BAD_REQUEST,
            message=message,
        ).model_dump(),
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@app.exception_handler(StarletteHTTPException)
async def global_exception_handler(_request: Request, e: Exception):
    if isinstance(e, UnauthorizedError):
        response = JSONResponse(
            content=FailResponse(
                errors='Unauthenticated.',
                message=e.message,
                code=e.code,
                subcode=e.subcode,
            ).model_dump(),
            status_code=e.code,
        )
        response.delete_cookie(REFRESH_KEY)
        return response

    if isinstance(e, CustomError):
        return JSONResponse(
            content=FailResponse(
                errors=str(e.__class__.__name__),
                message=e.message,
                code=e.code,
                subcode=e.subcode,
            ).model_dump(),
            status_code=e.code,
        )

    return JSONResponse(
        content=FailResponse(
            message='Could not process request. Try again later.',
        ).model_dump(),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.get('/health')
def health() -> dict:
    return {'status': 'ok'}
