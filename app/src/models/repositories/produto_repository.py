from typing import Dict, Tuple
from psycopg2.extensions import connection


class ProdutoRepository:
    def __init__(self, conn: connection) -> None:
        self.__conn = conn

    def registry_produto(self, produto_infos: Dict) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            INSERT INTO produtos
            (produto_nome, produto_preco)
            VALUES
            (%s, %s)
            RETURNING id
            """,
            (
                produto_infos["nome"],
                produto_infos["preco"],
            ),
        )
        id_produto = cursor.fetchone()[0]
        self.__conn.commit()
        return id_produto

    def find_produto_by_id(self, produto_id: int) -> Tuple:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT * FROM produtos WHERE id = %s
            """,
            (produto_id,),
        )
        user = cursor.fetchone()

        return user

    def delete_produto_by_id(self, produto_id: int) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            DELETE FROM produtos WHERE id = %s
            """,
            (produto_id,),
        )
        self.__conn.commit()

    def update_produto_by_id(self, produto_infos: Dict, produto_id: int) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            UPDATE produtos
            SET produto_nome = %s, produto_preco = %s
            WHERE id = %s
            """,
            (produto_infos["nome"], produto_infos["preco"], produto_id),
        )
        self.__conn.commit()
