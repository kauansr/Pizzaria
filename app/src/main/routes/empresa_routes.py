from flask import Blueprint, jsonify, request


empresa_routes_bp = Blueprint("empresa_routes", __name__)


from src.main.services.empresa_controller import EmpresaController
from src.main.auth.token import EmpresaToken, jwt_required, superadmin_required

from src.models.repositories.empresa_repository import EmpresaRepository
from src.models.repositories.login_repository import LoginRepository

from src.models.settings.db_connection_handler import db_connection_handler


@empresa_routes_bp.route("/empresa", methods=["POST"])
def create_empresa():
    conn = db_connection_handler.get_connection()
    empresa_repository = EmpresaRepository(conn)
    controller = EmpresaController(empresa_repository)

    response = controller.create(request.json)

    return jsonify(response["body"]), response["status_code"]


@empresa_routes_bp.route("/empresa/<empresa_id>", methods=["GET"])
@jwt_required
def find_empresa(empresa_id):
    conn = db_connection_handler.get_connection()
    empresa_repository = EmpresaRepository(conn)
    controller = EmpresaController(empresa_repository)

    response = controller.find(empresa_id)

    return jsonify(response["body"]), response["status_code"]


@empresa_routes_bp.route("/empresa/<empresa_id>", methods=["PUT"])
@superadmin_required
def update_empresa(empresa_id):
    conn = db_connection_handler.get_connection()
    empresa_repository = EmpresaRepository(conn)
    controller = EmpresaController(empresa_repository)

    response = controller.update(empresa_id, request.json)

    return jsonify(response["body"]), response["status_code"]


@empresa_routes_bp.route("/empresa/<empresa_id>", methods=["DELETE"])
@superadmin_required
def delete_empresa(empresa_id):
    conn = db_connection_handler.get_connection()
    empresa_repository = EmpresaRepository(conn)
    controller = EmpresaController(empresa_repository)

    response = controller.delete(empresa_id)

    return jsonify(response["body"]), response["status_code"]


@empresa_routes_bp.route("/empresa/token", methods=["POST"])
def login_empresa():
    conn = db_connection_handler.get_connection()
    login_repository = LoginRepository(conn)
    controller = EmpresaToken(login_repository)

    response = controller.create_token(request.json)

    return jsonify(response["body"]), response["status_code"]
