import uuid, datetime
from sqlalchemy.types import CHAR, Numeric
from sqlalchemy import String, DateTime, NUMERIC, ForeignKey, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.services.database import BaseClass
from app.models.models import *


class Transaction(BaseClass):
    __tablename__ = "transactions"
    transaction_id: Mapped[str] = mapped_column(
        CHAR(32),
        primary_key=True,
        unique=True,
        nullable=False,
        default=lambda: uuid.uuid4().hex,
    )
    user_id: Mapped[str] = mapped_column(
        CHAR(32), ForeignKey("users.user_id"), nullable=False
    )
    account_id: Mapped[str] = mapped_column(
        CHAR(32), ForeignKey("accounts.account_id"), nullable=False
    )
    category_id: Mapped[str] = mapped_column(
        CHAR(32), ForeignKey("categories.category_id"), nullable=False
    )
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[Numeric] = mapped_column(NUMERIC(10, 2), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(10), nullable=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)

    user = relationship("User")
    account = relationship("Account")
    category = relationship("Category")

    @classmethod
    async def create(cls, db: AsyncSession, transaction_id=None, **kwargs):
        if not transaction_id:
            transaction_id = uuid.uuid4().hex

        transaction = cls(transaction_id=transaction_id, **kwargs)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction

    @classmethod
    async def get(cls, db: AsyncSession, transaction_id: str, user_id: str):
        try:
            transaction = (
                (
                    await db.execute(
                        select(cls)
                        .filter(cls.transaction_id == transaction_id)
                        .filter(cls.user_id == user_id)
                    )
                )
                .scalars()
                .first()
            )
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def get_all(
        cls,
        db: AsyncSession,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
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
    async def get_by_category(
        cls,
        db: AsyncSession,
        user_id: str,
        category_id: str,
        skip: int = 0,
        limit: int = 100,
    ):
        try:
            transaction = (
                (
                    await db.execute(
                        select(cls)
                        .filter(cls.user_id == user_id)
                        .filter(cls.category_id == category_id)
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
    async def get_by_account(
        cls,
        db: AsyncSession,
        user_id: str,
        account_id: str,
        skip: int = 0,
        limit: int = 100,
    ):
        try:
            transaction = (
                (
                    await db.execute(
                        select(cls)
                        .filter(cls.user_id == user_id)
                        .filter(cls.account_id == account_id)
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
    async def update(
        cls, db: AsyncSession, transaction_id: str, user_id: str, **kwargs
    ):
        try:
            transaction = await cls.get(db, transaction_id, user_id)
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
    async def delete(cls, db: AsyncSession, transaction_id: str, user_id: str):
        try:
            transaction = await cls.get(db, transaction_id, user_id)
            if not transaction:
                return None
        except NoResultFound:
            return None
        await db.delete(transaction)
        await db.commit()
        return transaction
