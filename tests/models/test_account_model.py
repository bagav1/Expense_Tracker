from app.models.models import User, Account


class TestDBAccount:

    def test_successful_user_creation(self, session):
        user = User(name="Test User", email="test@example.com", password="password")
        account = Account(user=user, account_name="My Account", account_type="savings")

        session.add(account)
        session.commit()

        qry_account = (
            session.query(Account).filter_by(account_name="My Account").first()
        )

        assert qry_account is not None
        assert len(qry_account.account_id) == 32
        assert qry_account.user_id == user.user_id
        assert qry_account.account_name == "My Account"
        assert qry_account.account_type == "savings"
        assert qry_account.currency == "COP"
        assert qry_account.initial_balance == 0

    def test_initial_balance_decimal(self, session):
        user = User(name="Test User", email="test2@example.com", password="password")
        account = Account(
            user=user,
            account_name="My Account2",
            account_type="savings",
            currency="USD",
            initial_balance=12345,
        )

        session.add(account)
        session.commit()

        qry_account = (
            session.query(Account).filter_by(account_name="My Account2").first()
        )

        assert qry_account.currency != "COP"
        assert qry_account.initial_balance == 12345.00

    def test_initial_balance_max(self, session):
        user = User(name="Test User", email="test3@example.com", password="password")
        account = Account(
            user=user,
            account_name="My Account3",
            account_type="savings",
            initial_balance=123456780.12345,
        )

        session.add(account)
        session.commit()

        qry_account = (
            session.query(Account).filter_by(account_name="My Account3").first()
        )

        assert qry_account.currency == "COP"
        assert float(qry_account.initial_balance) == 123456780.12  # Max 2 decimal

    def test_account_user_relationship(self, session):
        user = User(name="Test User", email="test4@example.com", password="password")
        account = Account(user=user, account_name="My Account4", account_type="savings")

        session.add(user)
        session.add(account)
        session.commit()

        assert account.user == user
        assert account in user.accounts

    def test_get_user_accounts(self, session):
        user = User(name="Test User", email="test5@example.com", password="password")
        account1 = Account(user=user, account_name="Account 1", account_type="savings")
        account2 = Account(user=user, account_name="Account 2", account_type="savings")

        session.add_all([user, account1, account2])
        session.commit()

        assert user.accounts == [account1, account2]
