from allocations.adapters.repository import AbstractRepository
from allocations.domain.model import OrderLine
from allocations.service_layer import services


class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def delete(self, reference):
        self._batches.remove(reference)

    def list(self):
        return list(self._batches)


class FakeUnitOfWork:
    def __init__(self):
        self.batches = FakeRepository([])
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        pass

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_allocation_service_returns_batch_ref():
    uow = FakeUnitOfWork()
    services.add_batch(
        uow,
        reference="batch-001",
        sku="sku-RED-CHAIR",
        available_quantity=10,
    )
    allocated_batch_ref = services.allocate(
        OrderLine("order-001", "sku-RED-CHAIR", 2), uow
    )
    assert allocated_batch_ref == "batch-001"
