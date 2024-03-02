from datetime import datetime
from app.utils import DateFormat
from app.models.models import Category, Transaction, User, Account


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
            description="Test Transaction",
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
            description="Test Transaction",
        )

        session.add_all([category, transaction])
        session.commit()

        assert transaction.category == category
        assert transaction in category.transactions
