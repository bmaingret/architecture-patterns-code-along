from typing import Protocol
from allocation import Batch

class AbstractRepository(Protocol):
    def add(batch: Batch):
        pass

    def get(batch: Batch):
        pass

class SQLiteInMemoryRepository():
    

