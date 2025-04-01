from typing import Dict
from datetime import datetime


class PedidosController:
    def __init__(self, pedido_repository) -> None:
        self.__pedido_repository = pedido_repository

    def create(self, body) -> Dict:
        try:
            user_id = body.get("user_id")
            email = body.get("email")
            data_created = datetime.now()
            frete = body.get("frete")
            pedido_nome = body.get("nome")
            custo_total = body.get("custo_total")

            pedido_infos = {
                "user_id": user_id,
                "email": email,
                "data_create": data_created,
                "pedido_nome": pedido_nome,
                "status_pedido": "Preparando...",
                "frete": frete,
                "custo_total": custo_total,
            }

            id_pedido = self.__pedido_repository.registry_pedido(pedido_infos)

            return {"body": {"id": id_pedido, **pedido_infos}, "status_code": 201}

        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400,
            }

    def find(self, pedido_id: int) -> Dict:
        try:

            infos = self.__pedido_repository.find_pedido_by_id(pedido_id)

            if not infos:
                raise Exception("Pedido not found!")

            return {
                "body": {
                    "pedido": {
                        "id": infos[0],
                        "user_id": infos[1],
                        "email": infos[2],
                        "nome": infos[3],
                        "create_at": infos[4],
                        "status_entrega": infos[5],
                        "frete": infos[6],
                        "custo_total": infos[7],
                    }
                },
                "status_code": 200,
            }

        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 404,
            }

    def update(self, pedido_id: int, body: Dict) -> Dict:
        try:

            status_pedido = body.get("status_pedido")

            infos = self.__pedido_repository.find_pedido_by_id(pedido_id)

            if not infos:
                raise Exception("pedido not found!")

            if not status_pedido:
                status_pedido = infos[5]

            new_infos = {"status_pedido": status_pedido}

            self.__pedido_repository.update_pedido_by_id(new_infos, pedido_id)

            return {"body": {}, "status_code": 200}

        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400,
            }

    def delete(self, pedido_id: int) -> Dict:
        try:

            infos = self.__pedido_repository.find_pedido_by_id(pedido_id)

            if not infos:
                raise Exception("Pedido not found!")

            self.__pedido_repository.delete_pedido_by_id(pedido_id)

            return {"body": {}, "status_code": 204}

        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400,
            }
