from flask import jsonify, request, Blueprint


produto_routes_bp = Blueprint("produto_route", __name__)


from src.main.auth.token import superadmin_required

from src.main.services.produtos_controller import ProdutosController

from src.models.repositories.produto_repository import PedidoRepository


from src.models.settings.db_connection_handler import db_connection_handler


@produto_routes_bp.route("/produto", methods=["POST"])
@superadmin_required
def create_produto():
    conn = db_connection_handler.get_connection()
    produto_repository = PedidoRepository(conn)
    controller = ProdutosController(produto_repository)

    response = controller.create(request.json)

    return jsonify(response["body"]), response["status_code"]


@produto_routes_bp.route("/produto/<produto_id>", methods=["GET"])
def find_produto(produto_id):
    conn = db_connection_handler.get_connection()
    produto_repository = PedidoRepository(conn)
    controller = ProdutosController(produto_repository)

    response = controller.find(produto_id)

    return jsonify(response["body"]), response["status_code"]


@produto_routes_bp.route("/produto/<produto_id>", methods=["PUT"])
@superadmin_required
def update_produto(produto_id):
    conn = db_connection_handler.get_connection()
    produto_repository = PedidoRepository(conn)
    controller = ProdutosController(produto_repository)

    response = controller.update(produto_id, request.json)

    return jsonify(response["body"]), response["status_code"]


@produto_routes_bp.route("/produto/<produto_id>", methods=["DELETE"])
@superadmin_required
def delete_produto(produto_id):
    conn = db_connection_handler.get_connection()
    produto_repository = PedidoRepository(conn)
    controller = ProdutosController(produto_repository)

    response = controller.delete(produto_id)

    return jsonify(response["body"]), response["status_code"]
