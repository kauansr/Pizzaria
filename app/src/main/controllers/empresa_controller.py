from typing import Dict
from datetime import datetime
from src.main.auth.hash_data import HashBcrypt


class EmpresaController:
    def __init__(self, empresa_repository) -> None:
        self.__empresa_repository = empresa_repository
    
    def create(self, body) -> Dict:
        try:
            email = body.get("email")
            data_created = datetime.now()
            empresa_password = body.get("password")
            cnpj = body.get("cnpj")

            hashed_pass = HashBcrypt(empresa_password)

            password = hashed_pass.hash_password()

            empresa_infos = {"owner_email": email, "data_created": data_created, "cnpj":cnpj, "superadmin": True, "owner_password": password}

            id_empresa = self.__empresa_repository.registry_empresa(empresa_infos)

            return {
                "body": {"id": id_empresa, "owner_email": email, "data_created": data_created, "cnpj":cnpj, "superadmin": True},
                "status_code": 201
            }
        
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
    
    def find(self, empresa_id: int) -> Dict:
        try:
            
            infos = self.__empresa_repository.find_empresa_by_id(empresa_id)

            if not infos: raise Exception("Empresa not found!")

            return {
                "body": {
                    "empresa":{
                        "id": infos[0],
                        "email": infos[1],
                        "cnpj": infos[3],
                        "create_at": infos[2],
                        "superadmin": infos[4]
                    }},
                "status_code": 200
            }
        
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
    
    def update(self, empresa_id: int, body: Dict) -> Dict:
        try:

            empresa_new_email = body.get("email")
            cnpj = body.get("cnpj")
            
            infos = self.__empresa_repository.find_empresa_by_id(empresa_id)

            if not infos: raise Exception("User not found!")

            if not cnpj:
                cnpj = infos[3]
            
            if not empresa_new_email:
                empresa_new_email = infos[1]
            
            empresa_new_infos = {"email": empresa_new_email, "cnpj": cnpj}

            self.__empresa_repository.update_empresa_by_id(empresa_new_infos, empresa_id)

            return {
                "body": {},
                "status_code": 200
            }
        
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
    
    def delete(self, empresa_id: int) -> Dict:
        try:
            
            infos = self.__empresa_repository.find_empresa_by_id(empresa_id)

            if not infos: raise Exception("User not found!")

            self.__empresa_repository.delete_empresa_by_id(empresa_id)

            return {
                "body":{},
                "status_code": 204
            }
        
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }