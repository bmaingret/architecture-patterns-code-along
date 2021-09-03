from adapters.repository import SQLAlchemyRepository
from domain import model
from datetime import date


def test_flask_app_running(client):
    rv = client.get("/healthcheck")
    assert rv.status_code == 200


def test_allocation_endpoint_returns_batch_ref(session_on_disk, client):
    batch_warehouse = model.Batch("batch-001", "sku-RED-CHAIR", 10)
    batch_shipping = model.Batch("batch-002", "sku-RED-CHAIR", 10, eta=date.today())
    order_line = model.OrderLine("order-001", "sku-RED-CHAIR", 2)
    repo = SQLAlchemyRepository(session_on_disk)
    repo.add(batch_warehouse)
    repo.add(batch_shipping)
    session_on_disk.commit()

    rv = client.post(
        "/allocate",
        json={
            "order_reference": order_line.order_reference,
            "sku": order_line.sku,
            "quantity": order_line.quantity,
        },
    )
    assert rv.status_code == 201
    assert rv.get_json()["batch_ref"] == batch_warehouse.reference


def test_allocation_endpoint_persists_allocations(session_on_disk, client):
    batch_warehouse = model.Batch("batch-001", "sku-RED-CHAIR", 10)
    batch_shipping = model.Batch("batch-002", "sku-RED-CHAIR", 10, eta=date.today())
    order_line = model.OrderLine("order-001", "sku-RED-CHAIR", 10)
    repo = SQLAlchemyRepository(session_on_disk)
    repo.add(batch_warehouse)
    repo.add(batch_shipping)
    session_on_disk.commit()
    rv = client.post(
        "/allocate",
        json={
            "order_reference": order_line.order_reference,
            "sku": order_line.sku,
            "quantity": order_line.quantity,
        },
    )
    assert rv.status_code == 201
    assert rv.get_json()["batch_ref"] == batch_warehouse.reference

    rv = client.post(
        "/allocate",
        json={
            "order_reference": order_line.order_reference,
            "sku": order_line.sku,
            "quantity": order_line.quantity,
        },
    )
    assert rv.status_code == 201
    assert rv.get_json()["batch_ref"] == batch_shipping.reference
