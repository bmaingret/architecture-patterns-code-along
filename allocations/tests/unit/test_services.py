from adapters.repository import SQLAlchemyRepository
from domain.model import OrderLine
from service_layer import services


def test_allocation_service_returns_batch_ref(session_in_memory):
    repo = SQLAlchemyRepository(session_in_memory)
    services.add_batch(
        repo,
        session_in_memory,
        reference="batch-001",
        sku="sku-RED-CHAIR",
        available_quantity=10,
    )
    allocated_batch_ref = services.allocate(
        repo, session_in_memory, OrderLine("order-001", "sku-RED-CHAIR", 2)
    )
    assert allocated_batch_ref == "batch-001"
