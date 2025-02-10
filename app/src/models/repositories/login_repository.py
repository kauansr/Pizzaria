from typing import Tuple, Dict
from psycopg2.extensions import connection
from src.main.auth.hash_data import HashBcrypt

class LoginRepository:
    def __init__(self, conn: connection) -> None:
        self.__conn = conn
    

    def verify_user(self, user_infos: Dict) -> Tuple:    
        cursor = self.__conn.cursor()
        cursor.execute(
            '''
            SELECT userpassword FROM users WHERE email = %s
            ''', (user_infos["email"],)
        )
        hashed_password = cursor.fetchone()
        
        if hashed_password is None:
            return None

        verify_pass = HashBcrypt(user_infos['password'])
        if verify_pass.check_password(hashed_password[0]):
          
            cursor.execute(
                '''
                SELECT * FROM users WHERE email = %s
                ''', (user_infos["email"],)
            )
            user = cursor.fetchone()
            return user
        
        return None
    
    def verify_empresa(self, empresa_infos: Dict) -> Tuple:
        cursor = self.__conn.cursor()
        
        cursor.execute(
            '''
            SELECT owner_password FROM empresas WHERE owner_email = %s
            ''', (empresa_infos["email"],)
        )
        hashed_password = cursor.fetchone()
        
        if hashed_password is None:
            return None  

       
        verify_pass = HashBcrypt(empresa_infos["password"])
        if verify_pass.check_password(hashed_password[0].encode('utf-8')):
    
            cursor.execute(
                '''
                SELECT * FROM empresas WHERE owner_email = %s
                ''', (empresa_infos["email"],)
            )
            empresa = cursor.fetchone()
            return empresa
        
        return None