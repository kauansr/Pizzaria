from typing import Dict, Tuple
from psycopg2.extensions import connection
from absrepositories.abstract_empresa_repository import AbstractEmpresaRepository


class EmpresaRepository(AbstractEmpresaRepository):
    def __init__(self, conn: connection) -> None:
        self.__conn = conn

    def registry_empresa(self, empresa_infos: Dict) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            INSERT INTO empresas
            (owner_email, data_created, cnpj, superadmin, owner_password)
            VALUES
            (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                empresa_infos["owner_email"],
                empresa_infos["data_created"],
                empresa_infos["cnpj"],
                empresa_infos["superadmin"],
                empresa_infos["owner_password"],
            ),
        )

        id_empresa = cursor.fetchone()[0]
        self.__conn.commit()
        return id_empresa

    def find_empresa_by_id(self, empresa_id: int) -> Tuple:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT * FROM empresas WHERE id = %s
            """,
            (empresa_id,),
        )
        user = cursor.fetchone()

        return user

    def delete_empresa_by_id(self, empresa_id: int) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            DELETE FROM empresas WHERE id = %s
            """,
            (empresa_id,),
        )
        self.__conn.commit()

    def update_empresa_by_id(self, new_infos: Dict, empresa_id: int) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            UPDATE empresas
            SET owner_email = %s, cnpj = %s
            WHERE id = %s
            """,
            (new_infos["email"], new_infos["cnpj"], empresa_id),
        )
        self.__conn.commit()
