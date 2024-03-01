from datetime import datetime
from app.models.models import Category, Transaction, User, Account


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
            description="Test Transaction",
            payment_method="cash",
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
            description="Test Transaction",
            payment_method="cash",
        )

        session.add_all([user, account, transaction])
        session.commit()

        assert transaction.account.user == user
        assert transaction in user.accounts[0].transactions
