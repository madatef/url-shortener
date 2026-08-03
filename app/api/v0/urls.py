from collections.abc import Sequence

from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.url import UrlCreate, UrlResponse
from app.services.urls import create_url, delete_url, get_url_by_key, list_urls


router = APIRouter(prefix='/urls', tags=['urls'])


@router.post('', response_model=UrlResponse, status_code=status.HTTP_201_CREATED)
async def shorten(
    data: UrlCreate,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await create_url(session=session, value=data.value, user_id=user.id)


@router.get('', response_model=list[UrlResponse])
async def index(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Sequence[UrlResponse]:
    return await list_urls(session=session, user_id=user.id)


@router.delete('/{short_code}', status_code=status.HTTP_204_NO_CONTENT)
async def destroy(
    short_code: str,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:
    await delete_url(session=session, key=short_code, user_id=user.id)


# No get_current_user here: a short link has to resolve for whoever holds
# it. The auth cookie is scoped to path=/api so it is sent to this route
# too, but it is deliberately ignored.
@router.get(
    '/{short_code}',
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def follow(
    short_code: str,
    session: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    url = await get_url_by_key(session=session, key=short_code)

    # 307 rather than 301/308: browsers cache permanent redirects
    # indefinitely, which would keep serving a code after it is deleted.
    return RedirectResponse(
        url=url.value,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
