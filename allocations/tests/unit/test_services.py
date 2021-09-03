from adapters.repository import SQLAlchemyRepository
from domain.model import Batch, OrderLine
from service_layer import services
from datetime import date


def test_allocation_service_returns_batch_ref(session_in_memory):
    batch_warehouse = Batch("batch-001", "sku-RED-CHAIR", 10)
    batch_shipping = Batch("batch-002", "sku-RED-CHAIR", 10, eta=date.today())
    order_line = OrderLine("order-001", "sku-RED-CHAIR", 2)
    repo = SQLAlchemyRepository(session_in_memory)
    repo.add(batch_warehouse)
    repo.add(batch_shipping)
    session_in_memory.commit()
    allocated_batch_ref = services.allocate(order_line, repo, session_in_memory)
    assert allocated_batch_ref == batch_warehouse.reference
