import uuid
from sqlalchemy.types import CHAR, Numeric
from sqlalchemy import String, NUMERIC, ForeignKey, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.services.database import BaseClass
from app.models.models import *


class Account(BaseClass):
    __tablename__ = "accounts"
    account_id: Mapped[str] = mapped_column(
        CHAR(32),
        primary_key=True,
        unique=True,
        nullable=False,
        default=lambda: uuid.uuid4().hex,
    )
    user_id: Mapped[str] = mapped_column(
        CHAR(32), ForeignKey("users.user_id"), nullable=False
    )
    account_name: Mapped[str] = mapped_column(String(255), nullable=False)
    account_type: Mapped[str] = mapped_column(String(50), nullable=False)
    initial_balance: Mapped[Numeric] = mapped_column(
        NUMERIC(10, 2), default=0, server_default="0"
    )
    currency: Mapped[str] = mapped_column(
        String(3), nullable=False, default="COP", server_default="COP"
    )

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

    @classmethod
    async def create(cls, db: AsyncSession, account_id=None, **kwargs):
        if not account_id:
            account_id = uuid.uuid4().hex

        transaction = cls(account_id=account_id, **kwargs)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction

    @classmethod
    async def get(cls, db: AsyncSession, account_id: str, user_id: str):
        try:
            transaction = (
                (
                    await db.execute(
                        select(cls)
                        .filter(cls.account_id == account_id)
                        .filter(cls.user_id == user_id)
                    )
                )
                .scalars()
                .first()
            )
            if not transaction:
                return None
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def get_all(
        cls, db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100
    ):
        try:
            transaction = (
                (
                    await db.execute(
                        select(cls)
                        .filter(cls.user_id == user_id)
                        .offset(skip)
                        .limit(limit)
                    )
                )
                .scalars()
                .all()
            )
            if not transaction:
                return None
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def update(cls, db: AsyncSession, account_id: str, user_id: str, **kwargs):
        try:
            transaction = await cls.get(db, account_id, user_id)
            if not transaction:
                return None
        except NoResultFound:
            return None
        for key, value in kwargs.items():
            setattr(transaction, key, value)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction

    @classmethod
    async def delete(cls, db: AsyncSession, account_id: str, user_id: str):
        try:
            transaction = await cls.get(db, account_id, user_id)
            if not transaction:
                return None
        except NoResultFound:
            return None
        await db.delete(transaction)
        await db.commit()
        return transaction
