from typing import Dict
from datetime import datetime
from src.main.utils.hash_data import HashBcrypt


class UserController:
    def __init__(self, user_repository) -> None:
        self.__user_repository = user_repository
    
    def create(self, body) -> Dict:
        try:
            email = body.get("email")
            create_at = datetime.now()
            password = body.get("password")

            hashed_pass = HashBcrypt(password)

            userpassword = hashed_pass.hash_password()
            
            user_infos = {"email": email, "create_at": create_at, "password": userpassword}

            self.__user_repository.registry_user(user_infos)

            return {
                "body": {**user_infos},
                "status_code": 201
            }
        
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
    
    def find(self, user_id: int) -> Dict:
        try:
            
            infos = self.__user_repository.find_user_by_id(user_id)

            if not infos: raise Exception("User not found!")

            return {
                "body": {
                    "user":{
                        "id": infos[0],
                        "email": infos[1],
                        "create_at": infos[2]
                    }},
                "status_code": 200
            }
        
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
    
    def update(self, user_id: int, body: Dict) -> Dict:
        try:

            user_new_email = body.get("email")
            
            infos = self.__user_repository.find_user_by_id(user_id)

            if not infos: raise Exception("User not found!")

            self.__user_repository.update_user_by_id(user_new_email, user_id)

            return {
                "body": {},
                "status_code": 200
            }
        
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
    
    def delete(self, user_id: int) -> Dict:
        try:
            
            infos = self.__user_repository.find_user_by_id(user_id)

            if not infos: raise Exception("User not found!")

            self.__user_repository.delete_user_by_id(user_id)

            return {
                "body":{},
                "status_code": 204
            }
        
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }