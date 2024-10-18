from flask import jsonify, request, Blueprint


pedido_routes_bp = Blueprint("pedido_route", __name__)


from src.main.controllers.pedidos_controller import PedidosController

from src.models.repositories.pedido_repository import PedidoRepository


from src.models.settings.db_connection_handler import db_connection_handler


@pedido_routes_bp.route("/pedido", methods=['POST'])
def create_pedido():
    conn = db_connection_handler.get_connection()
    pedido_repository = PedidoRepository(conn)
    controller = PedidosController(pedido_repository)

    response = controller.create(request.json)

    return jsonify(response["body"]), response["status_code"]

@pedido_routes_bp.route("/pedido/<pedido_id>", methods=['GET'])
def find_pedido(pedido_id):
    conn = db_connection_handler.get_connection()
    pedido_repository = PedidoRepository(conn)
    controller = PedidosController(pedido_repository)

    response = controller.find(pedido_id)

    return jsonify(response["body"]), response["status_code"]

@pedido_routes_bp.route("/pedido/<pedido_id>", methods=['PUT'])
def update_pedido(pedido_id):
    conn = db_connection_handler.get_connection()
    pedido_repository = PedidoRepository(conn)
    controller = PedidosController(pedido_repository)

    response = controller.update(pedido_id, request.json)

    return jsonify(response["body"]), response["status_code"]

@pedido_routes_bp.route("/pedido/<pedido_id>", methods=['DELETE'])
def delete_pedido(pedido_id):
    conn = db_connection_handler.get_connection()
    pedido_repository = PedidoRepository(conn)
    controller = PedidosController(pedido_repository)

    response = controller.delete(pedido_id)

    return jsonify(response["body"]), response["status_code"]