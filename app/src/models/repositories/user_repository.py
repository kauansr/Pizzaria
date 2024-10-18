from typing import Dict, Tuple
from sqlite3 import Connection


class UserRepository:
    def __init__(self, conn: Connection) -> None:
        self.__conn = conn

    def registry_user(self, user_infos: Dict) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            '''
            INSERT INTO users
            (email, create_at, userpassword)
            VALUES
            (%s, %s, %s)
            ''', (
                user_infos["email"],
                user_infos["create_at"],
                user_infos["password"]
            )
        )
        self.__conn.commit()
    
    def find_user_by_id(self, user_id: int) -> Tuple:
        cursor = self.__conn.cursor()
        cursor.execute(
            '''
            SELECT * FROM users WHERE id = %s
            ''', (user_id,)
        )
        user = cursor.fetchone()

        return user
    
    def delete_user_by_id(self, user_id: int) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            '''
            DELETE FROM users WHERE id = %s
            ''', (user_id,)
        )
        self.__conn.commit()
    
    def update_user_by_id(self, new_email: str, user_id: int) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            '''
            UPDATE users
            SET email = %s
            WHERE id = %s
            ''', (new_email, user_id)
        )
        self.__conn.commit()