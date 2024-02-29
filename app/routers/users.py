from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from app.dependencies import get_current_user
from app.services.database import get_db
from app.schemas.schemas import UserBase, User
from app.models.models import User as UserModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=User, dependencies=[])
async def create_user(user: UserBase, db: AsyncSession = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    try:
        user = await UserModel.create(
            db,
            **{"name": user.name, "email": user.email, "password": hashed_password}
            # name=user.name, email=user.email, password=hashed_password
        )
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )


@router.get("/", response_model=list[User])
async def read_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    users = await UserModel.get_all(db, skip=skip, limit=limit)
    users_without_password = []
    for user in users:
        user_dict = user.__dict__
        user_dict.update({"password": "hidden"})
        users_without_password.append(user_dict)
    return users_without_password


@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this resource",
        )
    user = await UserModel.get(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_dict = user.__dict__
    user_dict.update({"password": "hidden"})
    return user_dict


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    user: UserBase,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this resource",
        )
    db_user = await UserModel.update(db, user_id, **user.model_dump())
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_dict = db_user.__dict__
    user_dict.update({"password": "hidden"})
    return user_dict


@router.delete("/{user_id}", response_model=User)
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this resource",
        )
    db_user = await UserModel.delete(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_dict = db_user.__dict__
    user_dict.update({"password": "hidden"})
    return user_dict
