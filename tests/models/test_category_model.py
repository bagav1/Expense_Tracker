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

    def test_category_user_relationship(self, session):
        user = User(name="Test User", email="test@example.com", password="password")
        category = Category(user=user, category_name="Food", category_type="expense")

        session.add(user)
        session.add(category)
        session.commit()

        assert category.user == user
        assert category in user.categories

    def test_reassign_category_to_transaction(self, session):
        user = User(name="Test User", email="test2@example.com", password="password")
        account = Account(user=user, account_name="My Account", account_type="savings")
        food = Category(user=user, category_name="Food", category_type="expense")
        transport = Category(
            user=user, category_name="Transport", category_type="expense"
        )

        transaction = Transaction(
            user=user,
            category=food,
            account=account,
            date=datetime.now(),
            amount=50,
            transaction_type="expense",
        )

        session.add_all([food, transport, transaction])
        session.commit()

        transaction.category = transport
        session.commit()

        assert transaction not in food.transactions
        assert transaction in transport.transactions

    def test_transaction_category_relationship(self, session):
        user = User(name="Test User", email="test3@example.com", password="password")
        account = Account(user=user, account_name="My Account", account_type="savings")
        category = Category(user=user, category_name="Food", category_type="expense")
        transaction = Transaction(
            user=user,
            category=category,
            account=account,
            date=datetime.now(),
            amount=50,
            transaction_type="expense",
        )

        session.add_all([category, transaction])
        session.commit()

        assert transaction.category == category
        assert transaction in category.transactions
