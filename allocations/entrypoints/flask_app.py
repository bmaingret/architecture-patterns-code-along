from datetime import date
from flask import Flask, request, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
from allocations.domain import model
from allocations.service_layer import services, unit_of_work


def create_app(engine, test_config=None):
    app = Flask(__name__)
    session_maker = scoped_session(sessionmaker(bind=engine))

    @app.route("/healthcheck")
    def healthcheck():
        return "OK", 200

    @app.route("/allocate", methods=["POST"])
    def allocate():
        data = request.get_json()
        assert data is not None
        line_to_allocate = model.OrderLine(
            data["order_reference"],
            data["sku"],
            data["quantity"],
        )
        batch_ref = services.allocate(
            line_to_allocate, unit_of_work.SQLAlchemyUnitOfWork(session_maker)
        )
        return jsonify({"batch_ref": batch_ref}), 201

    @app.route("/add_batch", methods=["POST"])
    def add_batch():
        data = request.get_json()
        assert data is not None
        eta = data.get("eta")
        if eta is None:
            eta = date.today()
        batch_ref = services.add_batch(
            unit_of_work.SQLAlchemyUnitOfWork(session_maker),
            data["reference"],
            data["sku"],
            data["available_quantity"],
            eta,
        )
        return jsonify({"batch_ref": batch_ref}), 201

    return app
