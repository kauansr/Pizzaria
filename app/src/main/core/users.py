from typing import Dict


class Users:
    def __init__(self, email, create_at, password):
        self.email = email
        self.create_at = create_at
        self.password = password

    def to_dict(self) -> Dict:
        return {
            "email": self.email,
            "create_at": self.create_at,
            "password": self.password,
        }
