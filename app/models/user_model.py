import uuid
from sqlalchemy.types import CHAR, DateTime as DateTimeType
from sqlalchemy import String, DateTime, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.services.database import BaseClass
from app.models.models import *


class User(BaseClass):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(
        CHAR(32),
        primary_key=True,
        unique=True,
        nullable=False,
        default=lambda: uuid.uuid4().hex,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    registered_at: Mapped[DateTimeType] = mapped_column(
        DateTime, default=func.now(), server_default=func.now()
    )

    accounts = relationship("Account", back_populates="user", cascade="all, delete")
    categories = relationship("Category", back_populates="user", cascade="all, delete")
    transactions = relationship(
        "Transaction", back_populates="user", cascade="all, delete"
    )

    @classmethod
    async def create(cls, db: AsyncSession, user_id=None, **kwargs):
        if not user_id:
            user_id = uuid.uuid4().hex

        transaction = cls(user_id=user_id, **kwargs)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction

    @classmethod
    async def get(cls, db: AsyncSession, user_id: str):
        try:
            transaction = await db.get(cls, user_id)
            if not transaction:
                return None
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def get_by_email(cls, db: AsyncSession, email: str):
        try:
            transaction = (
                (await db.execute(select(cls).filter(cls.email == email)))
                .scalars()
                .first()
            )
            if not transaction:
                return None
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def get_all(cls, db: AsyncSession, skip: int = 0, limit: int = 100):
        try:
            transaction = (
                (await db.execute(select(cls).offset(skip).limit(limit)))
                .scalars()
                .all()
            )
            if not transaction:
                return None
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def update(cls, db: AsyncSession, user_id: str, **kwargs):
        try:
            transaction = await db.get(cls, user_id)
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
    async def delete(cls, db: AsyncSession, user_id: str):
        try:
            transaction = await db.get(cls, user_id)
            if not transaction:
                return None
        except NoResultFound:
            return None
        await db.delete(transaction)
        await db.commit()
        return transaction
