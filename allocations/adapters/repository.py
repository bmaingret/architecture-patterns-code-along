from typing import Protocol, List
from allocations.domain.model import Batch
from abc import abstractmethod
from sqlalchemy.orm.exc import NoResultFound


class AbstractRepository(Protocol):
    @abstractmethod
    def add(self, batch: Batch) -> None:
        pass

    @abstractmethod
    def get(self, batch_reference: str) -> Batch:
        pass

    @abstractmethod
    def delete(self, batch_reference: str) -> None:
        pass

    @abstractmethod
    def list(self) -> List[Batch]:
        pass


class SQLAlchemyRepository:
    def __init__(self, session) -> None:
        self.session = session

    def add(self, batch: Batch) -> None:
        try:
            self.get(batch.reference)
        except NoResultFound:
            self.session.add(batch)

    def get(self, batch_reference: str) -> Batch:
        return (
            self.session.query(Batch).filter(Batch.reference == batch_reference).one()
        )

    def delete(self, batch_reference: str) -> None:
        to_delete = self.get(batch_reference)
        self.session.delete(to_delete)

    def list(self) -> List[Batch]:
        return self.session.query(Batch).all()
