from app.modules.auth.services.authorization import Principal, get_current_principal
from app.modules.auth.services.security import pwd_context
from app.modules.users.schemas.common import UserRegister, UserResponse
from app.shared.database.models import User
from app.shared.database.session import get_db_session
from app.shared.exceptions.http import ForbiddenException
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserRegister,
    session: AsyncSession = Depends(get_db_session),
) -> UserResponse:
    # Check if user already exists
    result = await session.execute(select(User).where(User.email == payload.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password (truncate to 72 chars for bcrypt compatibility)
    hashed_password = pwd_context.hash(payload.password[:72])

    # Create new user
    new_user = User(
        email=payload.email,
        password_hash=hashed_password,
        organization_id=payload.organization_id,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        organization_id=new_user.organization_id,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    principal: Principal = Depends(get_current_principal),
    session: AsyncSession = Depends(get_db_session),
) -> None:
    # Fetch the user to be deleted
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check permissions: users can only delete themselves unless they are an Admin or Owner
    if principal.user_id != str(user.id) and principal.role not in ["Admin", "Owner"]:
        raise ForbiddenException("You can only delete your own account")

    await session.delete(user)
    await session.commit()