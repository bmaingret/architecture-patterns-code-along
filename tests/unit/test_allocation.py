from datetime import date, timedelta
from allocations.domain.model import Batch, OrderLine, allocate


def test_allocating_same_line_twice_count_for_one_line():
    batch = Batch("batch-001", "sku-RED-CHAIR", 10)
    order_line = OrderLine("order-001", "sku-RED-CHAIR", 2)
    order_line_duplicated = OrderLine("order-001", "sku-RED-CHAIR", 2)
    batch._allocate(order_line)
    batch._allocate(order_line_duplicated)
    assert batch.available_quantity == 8


def test_cannot_allocate_if_not_same_sku():
    batch = Batch("batch-001", "sku-RED-CHAIR", 10)
    order_line = OrderLine("order-001", "sku-BLUE-TABLE", 2)
    assert batch.can_allocate(order_line) is False


def test_prefers_warehouse_to_shipping():
    batch_warehouse = Batch("batch-001", "sku-RED-CHAIR", 10)
    batch_shipping = Batch("batch-002", "sku-RED-CHAIR", 10, eta=date.today())
    order_line = OrderLine("order-001", "sku-RED-CHAIR", 2)
    allocated_batch = allocate(order_line, [batch_warehouse, batch_shipping])
    assert allocated_batch == batch_warehouse.reference


def test_prefers_shipping_if_not_warehouse():
    batch_warehouse = Batch("batch-001", "sku-BLUE-TABLE", 10)
    batch_shipping = Batch("batch-002", "sku-RED-CHAIR", 10, eta=date.today())
    order_line = OrderLine("order-001", "sku-RED-CHAIR", 2)
    allocated_batch = allocate(order_line, [batch_warehouse, batch_shipping])
    assert allocated_batch == batch_shipping.reference


def test_prefers_earlier_eta():
    batch_shipping_early = Batch("batch-001", "sku-RED-CHAIR", 10, eta=date.today())
    batch_shipping_late = Batch(
        "batch-002", "sku-RED-CHAIR", 10, eta=date.today() + timedelta(days=1)
    )
    order_line = OrderLine("order-001", "sku-RED-CHAIR", 2)
    allocated_batch = allocate(order_line, [batch_shipping_early, batch_shipping_late])
    assert allocated_batch == batch_shipping_early.reference
