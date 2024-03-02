from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import AccountBase, AccountResponse, AccountUpdate
from app.models.models import Account as AccountModel
from app.dependencies import get_current_user
from app.services.database import get_db

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=AccountResponse)
async def create_account(
    account: AccountBase,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    db_account = await AccountModel.create(
        db, **account.model_dump(), user_id=current_user_id
    )
    return db_account


@router.get("/", response_model=list[AccountResponse])
async def read_accounts(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    accounts = await AccountModel.get_all(
        db, user_id=current_user_id, skip=skip, limit=limit
    )
    return accounts


@router.get("/{account_id}", response_model=AccountResponse)
async def read_account(
    account_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    account = await AccountModel.get(db, account_id=account_id, user_id=current_user_id)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return account


@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: str,
    account: AccountUpdate,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    updated_account = await AccountModel.update(
        db, account_id=account_id, user_id=current_user_id, **account.model_dump()
    )
    if not updated_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return updated_account


@router.delete("/{account_id}", response_model=AccountResponse)
async def delete_account(
    account_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    deleted_account = await AccountModel.delete(
        db, account_id=account_id, user_id=current_user_id
    )
    if not deleted_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return deleted_account
