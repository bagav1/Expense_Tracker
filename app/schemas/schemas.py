from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str = Field(..., title="User Name")
    email: str = Field(..., title="User Email")
    password: str = Field(..., title="User Password")


class User(UserBase):
    user_id: str = Field(title="User ID")

    class Config:
        from_attributes = True


class AccountBase(BaseModel):
    account_name: str = Field(..., title="Account Name")
    account_type: str = Field(..., title="Account Type")
    initial_balance: Optional[str] = Field(default=0.0, title="Initial Balance")
    currency: Optional[str] = Field(default="COP", title="Currency")


class Account(AccountBase):
    account_id: str = Field(title="Account ID")
    user_id: str = Field(title="User Account")

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    category_name: str = Field(..., title="Category Name")
    category_type: str = Field(..., title="Category Type")
    parent_id: Optional[str] = Field(None, title="Parent Category")


class Category(CategoryBase):
    category_id: str = Field(title="Category ID")
    user_id: str = Field(title="User Category")

    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    account_id: str = Field(..., title="Account Transaction")
    category_id: str = Field(..., title="Category Transaction")
    date: str | datetime = Field(..., title="Transaction Date")
    description: Optional[str] = Field(None, title="Transaction Description")
    amount: float = Field(..., title="Transaction Amount")
    transaction_type: str = Field(..., title="Transaction Type")
    payment_method: Optional[str] = Field(None, title="Payment Method")
    notes: Optional[str] = Field(None, title="Transaction Notes")


class Transaction(TransactionBase):
    transaction_id: str = Field(title="Transaction ID")
    user_id: str = Field(title="User Transaction")

    class Config:
        from_attributes = True
