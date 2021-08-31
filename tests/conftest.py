import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from allocations.orm_sqlalchemy import mapper_registry
from allocations.repository import SQLiteInMemoryRepository, AbstractRepository
from allocations.flask_app import create_app


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    mapper_registry.metadata.drop_all(bind=engine)


@pytest.fixture
def repo(session) -> AbstractRepository:
    repo = SQLiteInMemoryRepository(session)
    return repo


@pytest.fixture
def client(session):
    app = create_app(test_config={"TESTING": True}, session=session)
    with app.test_client() as client:
        yield client
