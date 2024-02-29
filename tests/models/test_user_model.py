import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import User, Account


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
    db = Session()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


class TestDBUser:

    def test_successful_user_creation(self, session):
        user = User(name="Test User", email="test@example.com", password="password")

        session.add(user)
        session.commit()

        qry_user = session.query(User).filter_by(email="test@example.com").first()

        assert qry_user is not None
        assert qry_user.name == "Test User"
        assert qry_user.email == "test@example.com"
        assert qry_user.password == "password"

    def test_on_delete_cascade(self, session):
        user = User(name="Test User 5", email="test5@example.com", password="password")
        account = Account(
            user=user, account_name="My Account 2", account_type="savings"
        )

        session.add_all([user, account])
        session.commit()

        session.delete(user)
        session.commit()

        assert session.query(User).filter_by(email="test5@example.com").first() is None
        assert (
            session.query(Account).filter_by(account_name="My Account 2").first()
            is None
        )

    def test_unique_email_constraint(self, session):
        user1 = User(name="User 1", email="test2@example.com", password="password1")
        user2 = User(name="User 2", email="test2@example.com", password="password2")

        session.add(user1)
        with pytest.raises(IntegrityError):
            session.add(user2)
            session.commit()
