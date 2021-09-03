import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from adapters.orm_sqlalchemy import mapper_registry
from entrypoints.flask_app import create_app


@pytest.fixture
def in_memory_engine():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session_in_memory(in_memory_engine):
    session_maker = scoped_session(sessionmaker(bind=in_memory_engine))
    session = session_maker()
    yield session


@pytest.fixture
def client(on_disk_engine):
    app = create_app(on_disk_engine, test_config={"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def on_disk_engine():
    engine = create_engine("sqlite:///test.db")
    mapper_registry.metadata.create_all(engine)
    yield engine
    mapper_registry.metadata.drop_all(engine)


@pytest.fixture
def session_on_disk(on_disk_engine):
    session_maker = scoped_session(sessionmaker(bind=on_disk_engine))
    session = session_maker()
    yield session
