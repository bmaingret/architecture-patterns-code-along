from abc import abstractmethod
from typing import Protocol
from allocations.adapters import repository


class AbstractUnitOfWork(Protocol):
    products: repository.AbstractRepository

    @abstractmethod
    def __enter__(self) -> "AbstractUnitOfWork":
        pass

    def __exit__(self, exn_type, exn_value, traceback):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass


class SQLAlchemyUnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.products = repository.SQLAlchemyRepository(self.session)
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
