from fastapi import Depends, APIRouter, Request, Response, status, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.users import create_user, login


router = APIRouter(prefix='/auth', tags=['auth'])

def set_token_cookie(response: Response, token: dict[str, str]) -> None:
    response.set_cookie(
        key='access_token',
        value=token.get('access_token'),
        httponly=True,
        secure=False,
        samesite='lax',
        path='/api',
        max_age=15 * 60,
        expires=token.get('expiry'),
    )

@router.post('/signup', response_model=UserResponse, status_code=201)
async def signup(
    data: UserCreate,
    response: Response,
    session: AsyncSession = Depends(get_db),
):
    user, token = await create_user(session, username=data.username, password=data.password)
    set_token_cookie(response, token)

    return user

@router.post('/login', response_model=UserResponse)
async def signin(
    data: UserLogin,
    response: Response,
    session: AsyncSession = Depends(get_db),
):
    user, token = await login(session=session, username=data.username, password=data.password)
    set_token_cookie(response, token)

    return user