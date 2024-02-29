import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Category, Transaction, User, Account


@pytest.fixture(scope="module")
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        pool_recycle=300,
        pool_pre_ping=True,
    )
    Session = sessionmaker(bind=engine)
    User.metadata.create_all(engine)
    Account.metadata.create_all(engine)
    Category.metadata.create_all(engine)
    Transaction.metadata.create_all(engine)
    db = Session()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


class TestDBCategory:
    def test_account_transaction_relationship(self, session):
        user = User(name="Test User", email="test@example.com", password="password")
        account = Account(user=user, account_name="My Account", account_type="savings")
        category = Category(user=user, category_name="Food", category_type="expense")

        transaction = Transaction(
            user=user,
            account=account,
            category=category,
            date=datetime.now(),
            amount=100,
            transaction_type="expense",
        )

        session.add_all([account, transaction])
        session.commit()

        assert transaction.account == account
        assert transaction in account.transactions

    def test_user_transaction_relationship(self, session):
        user = User(name="Test User", email="test2@example.com", password="password")
        account = Account(user=user, account_name="My Account", account_type="savings")
        category = Category(user=user, category_name="Food", category_type="expense")

        transaction = Transaction(
            user=user,
            account=account,
            category=category,
            date=datetime.now(),
            amount=100,
            transaction_type="expense",
        )

        session.add_all([user, account, transaction])
        session.commit()

        assert transaction.account.user == user
        assert transaction in user.accounts[0].transactions
