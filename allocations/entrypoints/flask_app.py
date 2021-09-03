from flask import Flask, request, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
from adapters.repository import SQLAlchemyRepository
from domain import model
from service_layer import services


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
        session = session_maker()
        repo = SQLAlchemyRepository(session)
        batch_ref = services.allocate(line_to_allocate, repo, session)
        return jsonify({"batch_ref": batch_ref}), 201

    return app
