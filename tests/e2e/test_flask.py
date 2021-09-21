from datetime import date


def test_flask_app_running(client):
    rv = client.get("/healthcheck")
    assert rv.status_code == 200


def add_batch_endpoint(client, reference, sku, available_quantity, eta=None):
    r = client.post(
        "/add_batch",
        json={
            "reference": reference,
            "sku": sku,
            "available_quantity": available_quantity,
            "eta": eta,
        },
    )
    assert r.status_code == 201


def test_allocation_endpoint_returns_batch_ref(client):
    add_batch_endpoint(client, "batch-001", "sku-RED-CHAIR", 10)
    add_batch_endpoint(client, "batch-002", "sku-RED-CHAIR", 10, eta=date.today())
    rv = client.post(
        "/allocate",
        json={
            "order_reference": "order-001",
            "sku": "sku-RED-CHAIR",
            "quantity": 2,
        },
    )
    assert rv.status_code == 201
    assert rv.get_json()["batch_ref"] == "batch-001"


def test_allocation_endpoint_persists_allocations(client):
    add_batch_endpoint(client, "batch-001", "sku-RED-CHAIR", 10)
    add_batch_endpoint(client, "batch-002", "sku-RED-CHAIR", 10, eta=date.today())
    rv = client.post(
        "/allocate",
        json={
            "order_reference": "order-001",
            "sku": "sku-RED-CHAIR",
            "quantity": 10,
        },
    )
    assert rv.status_code == 201
    assert rv.get_json()["batch_ref"] == "batch-001"

    rv = client.post(
        "/allocate",
        json={
            "order_reference": "order-002",
            "sku": "sku-RED-CHAIR",
            "quantity": 10,
        },
    )
    assert rv.status_code == 201
    assert rv.get_json()["batch_ref"] == "batch-002"
