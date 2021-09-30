from allocations.domain.model import OrderLine
from allocations.service_layer.unit_of_work import SQLAlchemyUnitOfWork
from allocations.service_layer.services import add_batch


def test_uow_can_allocate(session_factory):
    order_line = OrderLine("ref-A", "sku-A", 10)
    with SQLAlchemyUnitOfWork(session_factory) as uow:
        add_batch(uow, "ref-A", "sku-A", 10)
        product = uow.products.get("sku-A")
        print(product.sku)
        allocated_ref = product.allocate(order_line)
        uow.commit()
    assert allocated_ref == "ref-A"
