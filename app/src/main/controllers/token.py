from typing import Dict, Tuple
import jwt
from datetime import timedelta, datetime


class Token:
    def __init__(self, login_repository) -> None:
        self.__login_repository = login_repository
    
    def create_user_token(self, body) -> Dict:
        try:
            email = body.get("email")
            password = body.get("password")

            if not email:
                raise Exception("E-mail is blank!")
            
            if not password:
                raise Exception("Password is blank!")
            
            user_infos = {"email": email, "password": password}
            
            user = self.__login_repository.verify_user(user_infos)
            
        
            if not user:
                raise Exception("User not verify!")

            if user is None:
                raise Exception("User not verified!")
            
            data_user_verified = {"id": user[0], "email": user[1], "create_at": str(user[2]), "exp": datetime.now() + timedelta(days=1)}
            
            encoded_jwt = jwt.encode(data_user_verified, "secret_key", algorithm="HS256")

            return {
                "body": {
                    "token": encoded_jwt
                },
                "status_code": 200
            }
        
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
    
    def create_empresa_token(self, body) -> Dict:
        try:
            email = body.get("email")
            password = body.get("password")

            if not email:
                raise Exception("E-mail is blank!")
            
            if not password:
                raise Exception("Password is blank!")
            
            empresa_infos = {"email": email, "password": password}

            empresa = self.__login_repository.verify_empresa(empresa_infos)

            if not empresa:
                raise Exception("Empresa not verify!")
            
            data_empresa_verified = {"id": empresa[0], "email": empresa[1], "create_at": str(empresa[2]), "cnpj": empresa[3], "superadmin": empresa[4], 
                                     "exp": datetime.now() + timedelta(days=1)}
            
            encoded_jwt = jwt.encode(data_empresa_verified, "secret_key", algorithm="HS256")

            return {
                "body": {
                    "token": encoded_jwt
                },
                "status_code": 200
            }
        
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }