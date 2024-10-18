from flask import Blueprint, jsonify, request


user_routes_bp = Blueprint('user_routes', __name__)


from src.main.controllers.user_controller import UserController
from src.main.controllers.token import Token

from src.models.repositories.user_repository import UserRepository
from src.models.repositories.login_repository import LoginRepository


from src.models.settings.db_connection_handler import db_connection_handler



@user_routes_bp.route("/users", methods=['POST'])
def create_user():
    conn = db_connection_handler.get_connection()
    user_repository = UserRepository(conn)
    controller = UserController(user_repository)

    response = controller.create(request.json)

    return jsonify(response["body"]), response["status_code"]


@user_routes_bp.route("/users/<user_id>", methods=['GET'])
def find_user(user_id):
    conn = db_connection_handler.get_connection()
    user_repository = UserRepository(conn)
    controller = UserController(user_repository)

    response = controller.find(user_id)

    return jsonify(response["body"]), response["status_code"]

@user_routes_bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    conn = db_connection_handler.get_connection()
    user_repository = UserRepository(conn)
    controller = UserController(user_repository)

    response = controller.update(user_id, request.json)

    return jsonify(response["body"]), response["status_code"]

@user_routes_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = db_connection_handler.get_connection()
    user_repository = UserRepository(conn)
    controller = UserController(user_repository)

    response = controller.delete(user_id)

    return jsonify(response["body"]), response["status_code"]

@user_routes_bp.route("/token", methods=["POST"])
def login_user():
    conn = db_connection_handler.get_connection()
    login_repository = LoginRepository(conn)
    controller = Token(login_repository)

    response = controller.create_user_token(request.json)

    return jsonify(response["body"]), response["status_code"]