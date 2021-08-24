import pytest  # noqa: E401
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from allocations.orm_sqlalchemy import mapper_registry
import allocations.repository


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def repo(session) -> allocations.repository.AbstractRepository:
    repo = allocations.repository.SQLiteInMemoryRepository(session)
    return repo
