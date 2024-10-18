import psycopg2

class DBConnectionHandler:

    def __init__(self) -> None:
        self.__connection_name = "Pizzaria"
        self.__conn = None
    
    def connect(self) -> None:
        conn = psycopg2.connect(database=self.__connection_name, host="localhost", port="port", user="user", password="senha")
        self.__conn = conn
    
    def get_connection(self):
        return self.__conn


db_connection_handler = DBConnectionHandler()