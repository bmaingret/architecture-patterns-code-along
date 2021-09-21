from typing import Optional
from datetime import date
from allocations.domain import model
from allocations.service_layer.unit_of_work import AbstractUnitOfWork


def allocate(order_line: model.OrderLine, uow: AbstractUnitOfWork):
    with uow:
        allocated_ref = model.allocate(order_line, uow.batches.list())
        uow.commit()
    return allocated_ref


def add_batch(
    uow: AbstractUnitOfWork,
    reference: str,
    sku: str,
    available_quantity: int,
    eta: Optional[date] = None,
) -> None:
    with uow:
        uow.batches.add(
            model.Batch(
                reference=reference,
                sku=sku,
                available_quantity=available_quantity,
                eta=eta,
            )
        )
        uow.commit()
