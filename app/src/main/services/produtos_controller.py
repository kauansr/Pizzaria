from typing import Dict
from datetime import datetime


class ProdutosController:
    def __init__(self, produto_repository) -> None:
        self.__produto_repository = produto_repository
    
    def create(self, body) -> Dict:
        try:
            preco = body.get("preco")
            nome = body.get("nome")

            produto_infos = {"preco": preco, "nome": nome}

            self.__produto_repository.registry_produto(produto_infos)

            return {
                "body": {**produto_infos},
                "status_code": 201
            }
        
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
    
    def find(self, produto_id: int) -> Dict:
        try:
            
            infos = self.__produto_repository.find_produto_by_id(produto_id)

            if not infos: raise Exception("produto not found!")

            return {
                "body": {
                    "produto":{
                        "id": infos[0],
                        "nome": infos[1],
                        "preco": infos[2],
                        
                    }},
                "status_code": 200
            }
        
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
    
    def update(self, produto_id: int, body: Dict) -> Dict:
        try:

            new_preco = body.get("preco")
            nome = body.get("nome")
            
            infos = self.__produto_repository.find_produto_by_id(produto_id)

            if not infos: raise Exception("Produto not found!")

            if not nome:
                nome = infos[1]
            
            if not new_preco:
                new_preco = infos[2]
            
            new_infos = {"preco": new_preco, "nome": nome}

            self.__produto_repository.update_produto_by_id(new_infos, produto_id)

            return {
                "body": {},
                "status_code": 200
            }
        
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
    
    def delete(self, produto_id: int) -> Dict:
        try:
            
            infos = self.__produto_repository.find_produto_by_id(produto_id)

            if not infos: raise Exception("Produto not found!")

            self.__produto_repository.delete_produto_by_id(produto_id)

            return {
                "body":{},
                "status_code": 204
            }
        
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }