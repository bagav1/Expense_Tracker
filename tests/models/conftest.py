import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services.database import BaseClass


@pytest.fixture(scope="module")
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        pool_recycle=300,
        pool_pre_ping=True,
    )
    Session = sessionmaker(bind=engine)
    BaseClass.metadata.create_all(engine)
    db = Session()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        BaseClass.metadata.drop_all(engine)
