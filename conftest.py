import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from orm_sqlalchemy import map_allocations, mapper_registry

@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    mapper_registry.metadata.create_all(engine) 
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
