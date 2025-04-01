from typing import Dict


class Empresa:
    def __init__(self, owner_email, data_created, owner_password, cnpj, superadmin):
        self.owner_email = owner_email
        self.data_created = data_created
        self.owner_password = owner_password
        self.cnpj = cnpj
        self.superadmin = superadmin

    def to_dict(self) -> Dict:
        return {
            "owner_email": self.owner_email,
            "data_created": self.data_created,
            "owner_password": self.owner_password,
            "cnpj": self.cnpj,
            "superadmin": self.superadmin,
        }
