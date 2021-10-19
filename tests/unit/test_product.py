from allocations.domain.events import OutOfStockEvent
from allocations.domain.model import Batch, OrderLine, Product


def test_outofstock_product_should_raise_event():
    sku = "RED-CHAIR-1"
    batch = Batch("batch-001", sku, 0)
    prod = Product(sku=sku, batches=[batch])
    prod.allocate(OrderLine("order-001", sku, 1))
    assert prod.events[-1] == OutOfStockEvent(sku=sku)
