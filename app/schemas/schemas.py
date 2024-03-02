from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str = Field(..., title="User Name")
    email: str = Field(..., title="User Email")
    password: str = Field(..., title="User Password")


class UserResponse(UserBase):
    user_id: str = Field(title="User ID")

    class ConfigDict:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str = Field(title="User Name")
    email: str = Field(title="User Email")


class AccountBase(BaseModel):
    account_name: str = Field(..., title="Account Name")
    account_type: str = Field(..., title="Account Type")
    initial_balance: Optional[float] = Field(default=0.0, title="Initial Balance")
    currency: Optional[str] = Field(default="COP", title="Currency")


class AccountResponse(AccountBase):
    account_id: str = Field(title="Account ID")
    user_id: str = Field(title="User Account")

    class ConfigDict:
        from_attributes = True


class AccountUpdate(BaseModel):
    account_name: str = Field(title="Account Name")
    account_type: str = Field(title="Account Type")
    initial_balance: float = Field(title="Initial Balance")
    currency: str = Field(title="Currency")


class CategoryBase(BaseModel):
    category_name: str = Field(..., title="Category Name")
    category_type: str = Field(..., title="Category Type")
    parent_id: Optional[str] = Field(None, title="Parent Category")


class CategoryResponse(CategoryBase):
    category_id: str = Field(title="Category ID")
    user_id: str = Field(title="User Category")

    class ConfigDict:
        from_attributes = True


class CategoryUpdate(BaseModel):
    category_name: str = Field(title="Category Name")
    category_type: str = Field(title="Category Type")
    parent_id: Optional[str] = Field(None, title="Parent Category")


class TransactionBase(BaseModel):
    account_id: str = Field(..., title="Account Transaction")
    category_id: str = Field(..., title="Category Transaction")
    date: str | datetime = Field(..., title="Transaction Date")
    description: Optional[str] = Field(None, title="Transaction Description")
    amount: float = Field(..., title="Transaction Amount")
    transaction_type: str = Field(
        ..., title="Transaction Type", examples=["income", "expense"]
    )
    payment_method: str = Field(
        ...,
        title="Payment Method",
        examples=["Efectivo", "Tarjeta de crédito", "Transferencia"],
    )
    notes: Optional[str] = Field(None, title="Transaction Notes")


class TransactionResponse(TransactionBase):
    transaction_id: str = Field(title="Transaction ID")
    user_id: str = Field(title="User Transaction")

    class ConfigDict:
        from_attributes = True


class TransactionUpdate(BaseModel):
    account_id: str = Field(title="Account Transaction")
    category_id: str = Field(title="Category Transaction")
    date: str | datetime = Field(title="Transaction Date")
    description: str = Field(title="Transaction Description")
    transaction_type: str = Field(title="Transaction Type")
    payment_method: str = Field(title="Payment Method")
    notes: Optional[str] = Field(None, title="Transaction Notes")
