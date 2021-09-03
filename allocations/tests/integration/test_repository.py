from adapters.repository import SQLAlchemyRepository
from domain.model import Batch, OrderLine, allocate


def test_order_line_allocation(session_in_memory):
    repo = SQLAlchemyRepository(session_in_memory)
    batch = Batch("batch-001", "sku-RED-CHAIR", 2)
    order_line = OrderLine("order-001", "sku-RED-CHAIR", 2)
    allocate(order_line, [batch])
    repo.add(batch)
    session_in_memory.commit()
    result = repo.get(batch.reference)
    assert result._allocated_order_lines == batch._allocated_order_lines
