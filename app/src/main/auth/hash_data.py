import bcrypt
import base64


class HashBcrypt:
    def __init__(self, password: str):
        self.__password = password
    

    def hash_password(self) -> str:
      
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(self.__password.encode('utf-8'), salt)
        return base64.b64encode(hashed).decode('utf-8')

    def check_password(self, hashed_password: str) -> bool:

        decoded_hash = base64.b64decode(hashed_password)
        return bcrypt.checkpw(self.__password.encode('utf-8'), decoded_hash)