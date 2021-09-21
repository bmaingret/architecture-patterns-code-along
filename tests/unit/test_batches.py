from allocations.domain.model import Batch, OrderLine


def test_allocating_x_unit_reduce_quantity_by_x():
    batch = Batch("batch-001", "sku-RED-CHAIR", 10)
    order_line = OrderLine("order-001", "sku-RED-CHAIR", 2)
    batch._allocate(order_line)
    assert batch.available_quantity == 8


def test_can_allocate_if_available_equal_to_ordered():
    batch = Batch("batch-001", "sku-RED-CHAIR", 2)
    order_line = OrderLine("order-001", "sku-RED-CHAIR", 2)
    assert batch.can_allocate(order_line)


def test_cannot_allocate_if_available_less_than_ordered():
    batch = Batch("batch-001", "sku-RED-CHAIR", 1)
    order_line = OrderLine("order-001", "sku-RED-CHAIR", 2)
    assert batch.can_allocate(order_line) is False
