from typing import Optional
from datetime import date
from adapters.repository import AbstractRepository
from domain import model


def allocate(repo: AbstractRepository, session, order_line: model.OrderLine):
    allocated_ref = model.allocate(order_line, repo.list())
    session.commit()
    return allocated_ref


def add_batch(
    repo: AbstractRepository,
    session,
    reference: str,
    sku: str,
    available_quantity: int,
    eta: Optional[date] = None,
) -> None:
    repo.add(
        model.Batch(
            reference=reference, sku=sku, available_quantity=available_quantity, eta=eta
        )
    )
    session.commit()
    return
