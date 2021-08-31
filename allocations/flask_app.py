from flask import Flask, request, jsonify
from .repository import SQLiteInMemoryRepository
from . import model


def create_app(session, test_config=None):
    app = Flask(__name__)

    @app.route("/healthcheck")
    def healthcheck():
        return "OK", 200

    @app.route("/allocate", methods=["POST"])
    def allocate():
        line_to_allocate = model.OrderLine(
            request.json["order_reference"],
            request.json["sku"],
            request.json["quantity"],
        )
        repo = SQLiteInMemoryRepository(session)
        batch_ref = model.allocate(line_to_allocate, repo.list())
        session.commit()
        return jsonify({"batch_ref": batch_ref}), 201

    return app
