from adapters.repository import AbstractRepository
from domain import model


def allocate(order_line: model.OrderLine, repo: AbstractRepository, session):
    allocated_ref = model.allocate(order_line, repo.list())
    session.commit()
    return allocated_ref
