import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

class DBConnectionHandler:

    def __init__(self) -> None:
        self.__connection_name = os.getenv("DB_NAME")
        self.__conn = None
    
    def connect(self) -> None:
        conn = psycopg2.connect(
            database=self.__connection_name, 
            host=os.getenv("DB_HOST"), 
            port=os.getenv("DB_PORT"), 
            user=os.getenv("DB_USERNAME"), 
            password=os.getenv("DB_PASSWORD")
            )
        self.__conn = conn
    
    def get_connection(self):
        return self.__conn


db_connection_handler = DBConnectionHandler()