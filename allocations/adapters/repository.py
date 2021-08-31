from typing import Protocol, List
from domain.model import Batch
from abc import abstractmethod


class AbstractRepository(Protocol):
    @abstractmethod
    def add(self, batch: Batch) -> None:
        pass

    @abstractmethod
    def get(self, batch_reference: str) -> Batch:
        pass

    @abstractmethod
    def list(self) -> List[Batch]:
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

    def list(self) -> List[Batch]:
        return self.session.query(Batch).all()


class FakeRepository:
    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)
