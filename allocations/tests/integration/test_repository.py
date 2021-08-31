from domain.model import Batch, OrderLine, allocate


def test_order_line_allocation(session, repo):
    batch = Batch("batch-001", "sku-RED-CHAIR", 2)
    order_line = OrderLine("order-001", "sku-RED-CHAIR", 2)
    allocate(order_line, [batch])
    repo.add(batch)
    session.commit()
    result = repo.get(batch.reference)
    assert result._allocated_order_lines == batch._allocated_order_lines
