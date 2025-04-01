from flask import jsonify, request, Blueprint


pedido_routes_bp = Blueprint("pedido_route", __name__)


from src.main.auth.token import jwt_required, superadmin_required


from src.main.services.pedidos_controller import PedidosController

from src.models.repositories.pedido_repository import PedidoRepository


from src.models.settings.db_connection_handler import db_connection_handler


@pedido_routes_bp.route("/pedido", methods=["POST"])
@jwt_required
def create_pedido():
    conn = db_connection_handler.get_connection()
    pedido_repository = PedidoRepository(conn)
    controller = PedidosController(pedido_repository)

    response = controller.create(request.json)

    return jsonify(response["body"]), response["status_code"]


@pedido_routes_bp.route("/pedido/<pedido_id>", methods=["GET"])
@jwt_required
def find_pedido(pedido_id):
    conn = db_connection_handler.get_connection()
    pedido_repository = PedidoRepository(conn)
    controller = PedidosController(pedido_repository)

    response = controller.find(pedido_id)

    return jsonify(response["body"]), response["status_code"]


@pedido_routes_bp.route("/pedido/<pedido_id>", methods=["PUT"])
@superadmin_required
def update_pedido(pedido_id):
    conn = db_connection_handler.get_connection()
    pedido_repository = PedidoRepository(conn)
    controller = PedidosController(pedido_repository)

    response = controller.update(pedido_id, request.json)

    return jsonify(response["body"]), response["status_code"]


@pedido_routes_bp.route("/pedido/<pedido_id>", methods=["DELETE"])
@jwt_required
def delete_pedido(pedido_id):
    conn = db_connection_handler.get_connection()
    pedido_repository = PedidoRepository(conn)
    controller = PedidosController(pedido_repository)

    response = controller.delete(pedido_id)

    return jsonify(response["body"]), response["status_code"]
