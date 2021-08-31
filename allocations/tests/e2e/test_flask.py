from adapters.repository import SQLiteInMemoryRepository
from domain import model
from datetime import date


def test_flask_app_running(client):
    rv = client.get("/healthcheck")
    assert rv.status_code == 200


def test_allocation_endpoint_returns_batch_ref(session, client):
    batch_warehouse = model.Batch("batch-001", "sku-RED-CHAIR", 10)
    batch_shipping = model.Batch("batch-002", "sku-RED-CHAIR", 10, eta=date.today())
    order_line = model.OrderLine("order-001", "sku-RED-CHAIR", 2)
    repo = SQLiteInMemoryRepository(session)
    repo.add(batch_warehouse)
    repo.add(batch_shipping)
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


def test_allocation_endpoint_persists_allocations(session, client):
    batch_warehouse = model.Batch("batch-001", "sku-RED-CHAIR", 10)
    batch_shipping = model.Batch("batch-002", "sku-RED-CHAIR", 10, eta=date.today())
    order_line = model.OrderLine("order-001", "sku-RED-CHAIR", 10)
    repo = SQLiteInMemoryRepository(session)
    repo.add(batch_warehouse)
    repo.add(batch_shipping)
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
