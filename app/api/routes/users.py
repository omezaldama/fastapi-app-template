from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_req_user_id
from app.api.schemas.responses.common_responses import SuccessResponse
from app.api.schemas.responses.users_responses import MeResponse
from app.db.database import get_db
from app.services.users.users_service import UsersService


router = APIRouter()


@router.get('/me',
            response_model=SuccessResponse[MeResponse],
            status_code=status.HTTP_200_OK)
def me(
    *,
    session: Session = Depends(get_db),
    user_id: UUID = Depends(get_req_user_id),
):
    me = UsersService(session).get_user_by_id(user_id)
    return SuccessResponse[MeResponse](data=me)
