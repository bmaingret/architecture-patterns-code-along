from domain.model import Batch, OrderLine, allocate


def test_can_save_and_read_order_line(session):
    order_line = OrderLine("ref-A", "sku-A", 10)
    session.add(order_line)
    session.commit()
    result = session.query(OrderLine).filter(OrderLine.order_reference == "ref-A").one()
    assert order_line == result


def test_can_save_and_read_multiple_order_line(session):
    order_line_A = OrderLine("ref-A", "sku-A", 10)
    order_line_B = OrderLine("ref-B", "sku-A", 10)
    order_line_C = OrderLine("ref-C", "sku-A", 10)
    session.add(order_line_A)
    session.add(order_line_B)
    session.add(order_line_C)
    session.commit()
    result = session.query(OrderLine).all()
    assert result == [order_line_A, order_line_B, order_line_C]


def test_can_save_and_read_batch(session):
    batch_A = Batch("ref-A", "sku-A", 10)
    session.add(batch_A)
    session.commit()
    result = session.query(Batch).one()
    assert result == batch_A


def test_can_save_and_read_multiple_batches(session):
    batch_A = Batch("ref-A", "sku-A", 10)
    session.add(batch_A)
    batch_B = Batch("ref-B", "sku-B", 10)
    session.add(batch_B)
    batch_C = Batch("ref-C", "sku-C", 10)
    session.add(batch_C)
    session.commit()
    result = session.query(Batch).all()
    assert result == [batch_A, batch_B, batch_C]


def test_order_line_allocation(session):
    batch = Batch("batch-001", "sku-RED-CHAIR", 2)
    order_line = OrderLine("order-001", "sku-RED-CHAIR", 2)
    allocate(order_line, [batch])
    session.add(batch)
    session.commit()
    result = session.query(Batch).one()
    assert result._allocated_order_lines == batch._allocated_order_lines  # type: ignore


def test_order_line_allocation_external_table(session):
    batch = Batch("batch-001", "sku-RED-CHAIR", 2)
    order_line = OrderLine("order-001", "sku-RED-CHAIR", 2)
    allocate(order_line, [batch])
    session.add(batch)
    session.commit()
    result = dict(session.execute("SELECT * from  allocations").one())
    assert (result["batch_id"], result["order_line_id"]) == (batch.id, order_line.id)  # type: ignore
