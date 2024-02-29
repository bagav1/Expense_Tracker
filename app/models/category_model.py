import uuid
from sqlalchemy.types import CHAR
from sqlalchemy import String, ForeignKey, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.services.database import BaseClass
from app.models.models import *


class Category(BaseClass):
    __tablename__ = "categories"
    category_id: Mapped[str] = mapped_column(
        CHAR(32),
        primary_key=True,
        unique=True,
        nullable=False,
        default=lambda: uuid.uuid4().hex,
    )
    user_id: Mapped[str] = mapped_column(
        CHAR(32), ForeignKey("users.user_id"), nullable=False
    )
    category_name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_type: Mapped[str] = mapped_column(String(50), nullable=False)
    parent_id: Mapped[str] = mapped_column(
        CHAR(32), ForeignKey("categories.category_id"), nullable=True
    )

    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")

    @classmethod
    async def create(cls, db: AsyncSession, category_id=None, **kwargs):
        if not category_id:
            category_id = uuid.uuid4().hex

        transaction = cls(category_id=category_id, **kwargs)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction

    @classmethod
    async def get(cls, db: AsyncSession, category_id: str, user_id: str):
        try:
            transaction = (
                (
                    await db.execute(
                        select(cls)
                        .filter(cls.category_id == category_id)
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
    async def get_by_parent(
        cls,
        db: AsyncSession,
        user_id: str,
        parent_id: str,
        skip: int = 0,
        limit: int = 100,
    ):
        try:
            transaction = (
                (
                    await db.execute(
                        select(cls)
                        .filter(cls.user_id == user_id)
                        .filter(cls.parent_id == parent_id)
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
    async def update(cls, db: AsyncSession, category_id: str, user_id: str, **kwargs):
        try:
            transaction = await cls.get(db, category_id, user_id)
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
    async def delete(cls, db: AsyncSession, category_id: str, user_id: str):
        try:
            transaction = await cls.get(db, category_id, user_id)
            if not transaction:
                return None
        except NoResultFound:
            return None
        await db.delete(transaction)
        await db.commit()
        return transaction
