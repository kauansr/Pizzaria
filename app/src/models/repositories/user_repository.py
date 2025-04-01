from typing import Dict, Tuple
from psycopg2.extensions import connection
from absrepositories.abstract_user_repository import AbstractUserRepository


class UserRepository(AbstractUserRepository):
    def __init__(self, conn: connection) -> None:
        self.__conn = conn

    def registry_user(self, user_infos: Dict) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            INSERT INTO users
            (email, create_at, userpassword)
            VALUES
            (%s, %s, %s)
            RETURNING id
            """,
            (user_infos["email"], user_infos["create_at"], user_infos["password"]),
        )
        id_user = cursor.fetchone()[0]
        self.__conn.commit()
        return id_user

    def find_user_by_id(self, user_id: int) -> Tuple:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT * FROM users WHERE id = %s
            """,
            (user_id,),
        )
        user = cursor.fetchone()

        return user

    def delete_user_by_id(self, user_id: int) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            DELETE FROM users WHERE id = %s
            """,
            (user_id,),
        )
        self.__conn.commit()

    def update_user_by_id(self, new_email: str, user_id: int) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET email = %s
            WHERE id = %s
            """,
            (new_email, user_id),
        )
        self.__conn.commit()
