from typing import Dict
import jwt
from datetime import timedelta, datetime
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from functools import wraps
from flask import request, jsonify, g



load_dotenv()


class Token(ABC):
    def __init__(self, login_repository) -> None:
        self._login_repository = login_repository

    @abstractmethod
    def create_token(self, body: Dict) -> Dict:
        pass
    
    def decode_token(self, token: str):
        try:
            decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            return decoded_token
        except jwt.ExpiredSignatureError as je:
            raise Exception("Token expired!")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token!")


class UserToken(Token):

    def create_token(self, body: Dict) -> Dict:
        try:
            email = body.get("email")
            password = body.get("password")

            if not email:
                raise Exception("E-mail is blank!")
            
            if not password:
                raise Exception("Password is blank!")
            
            user_infos = {"email": email, "password": password}
            
            user = self._login_repository.verify_user(user_infos)
            
        
            if not user:
                raise Exception("User not verify!")

            if user is None:
                raise Exception("User not verified!")
            
            data_user_verified = {"id": user[0], "email": user[1], "create_at": str(user[2]), "exp": datetime.now() + timedelta(days=1)}
            
            encoded_jwt = jwt.encode(data_user_verified, os.getenv("SECRET_KEY"), algorithm="HS256")

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


class EmpresaToken(Token):

    def create_token(self, body: Dict) -> Dict:
        try:
            email = body.get("email")
            password = body.get("password")

            if not email:
                raise Exception("E-mail is blank!")
            
            if not password:
                raise Exception("Password is blank!")
            
            empresa_infos = {"email": email, "password": password}

            empresa = self._login_repository.verify_empresa(empresa_infos)

            if not empresa:
                raise Exception("Empresa not verify!")
            
            data_empresa_verified = {"id": empresa[0], "email": empresa[1], "create_at": str(empresa[2]), "cnpj": empresa[3], "superadmin": empresa[4], 
                                     "exp": datetime.now() + timedelta(days=1)}
            
            encoded_jwt = jwt.encode(data_empresa_verified, os.getenv("SECRET_KEY"), algorithm="HS256")

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
    
    def is_admin(self, token: str) -> bool:
        try:
            decoded_token = self.decode_token(token)
            if decoded_token and isinstance(decoded_token, dict):
                return decoded_token.get("superadmin", False)
            return False
        except Exception:
            return False
        

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

       
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1] 
        
        if not token:
            return jsonify({"error": "Token is empty!"}), 403

        try:
        
            user_token = UserToken(login_repository=None) 


            decoded_token = user_token.decode_token(token)

            g.user = decoded_token

        except Exception as e:
            return jsonify({"error": "Token invalid!", "message": str(e)}), 401

        return f(*args, **kwargs)

    return decorated_function

def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization').split(' ')[1]
        empresa_token = EmpresaToken(login_repository=None)
        
        
        if empresa_token.is_admin(token):
            return f(*args, **kwargs) 
        else:
            return jsonify({"error": "Unauthorized!"}), 403

    return decorated_function