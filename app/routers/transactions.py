from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import TransactionBase, TransactionResponse, TransactionUpdate
from app.models.models import Transaction as TransactionModel
from app.dependencies import get_current_user
from app.services.database import get_db
from app.utils import DateFormat

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionBase,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    model = transaction.model_dump()
    model.update({"date": DateFormat.from_iso(model.get("date", "")).to_local()})
    db_transaction = await TransactionModel.create(db, **model, user_id=current_user_id)
    return db_transaction


@router.get("/", response_model=list[TransactionResponse])
async def read_transactions(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    transactions = await TransactionModel.get_all(
        db, user_id=current_user_id, skip=skip, limit=limit
    )
    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def read_transaction(
    transaction_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    transaction = await TransactionModel.get(
        db, transaction_id=transaction_id, user_id=current_user_id
    )
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )
    return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    transaction: TransactionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    model = transaction.model_dump()
    model.update({"date": DateFormat.from_iso(model.get("date", "")).to_local()})
    updated_transaction = await TransactionModel.update(
        db, transaction_id=transaction_id, user_id=current_user_id, **model
    )
    if not updated_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )
    return updated_transaction


@router.delete("/{transaction_id}", response_model=TransactionResponse)
async def delete_transaction(
    transaction_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    deleted_transaction = await TransactionModel.delete(
        db, transaction_id=transaction_id, user_id=current_user_id
    )
    if not deleted_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )
    return deleted_transaction
