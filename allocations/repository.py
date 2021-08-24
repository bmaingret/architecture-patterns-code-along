from typing import Protocol
from allocations.model import Batch
from abc import abstractmethod


class AbstractRepository(Protocol):
    @abstractmethod
    def add(self, batch: Batch) -> None:
        pass

    @abstractmethod
    def get(self, batch_reference: str) -> Batch:
        pass


class SQLiteInMemoryRepository:
    def __init__(self, session) -> None:
        self.session = session

    def add(self, batch: Batch) -> None:
        self.session.add(batch)

    def get(self, batch_reference: str) -> Batch:
        return (
            self.session.query(Batch).filter(Batch.reference == batch_reference).one()
        )
