from typing import Dict, Tuple
from psycopg2.extensions import connection


class PedidoRepository:
    def __init__(self, conn: connection) -> None:
        self.__conn = conn

    def registry_pedido(self, pedido_infos: Dict) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            '''
            INSERT INTO pedidos
            (user_id, user_email, pedido_nome, data_create, status_pedido, frete, custo_total)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                pedido_infos["user_id"],
                pedido_infos["email"],
                pedido_infos["pedido_nome"],
                pedido_infos["data_create"],
                pedido_infos["status_pedido"],
                pedido_infos["frete"],
                pedido_infos["custo_total"]
            )
        )
        self.__conn.commit()
    
    def find_pedido_by_id(self, pedido_id: int) -> Tuple:
        cursor = self.__conn.cursor()
        cursor.execute(
            '''
            SELECT * FROM pedidos WHERE id = %s
            ''', (pedido_id,)
        )
        pedido = cursor.fetchone()

        return pedido
    
    def delete_pedido_by_id(self, pedido_id: int) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            '''
            DELETE FROM pedidos WHERE id = %s
            ''', (pedido_id,)
        )
        self.__conn.commit()
    
    def update_pedido_by_id(self, new_infos: Dict, pedido_id: int) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            '''
            UPDATE pedidos
            SET status_pedido = %s
            WHERE id = %s
            ''', (new_infos["status_pedido"], pedido_id)
        )
        self.__conn.commit()