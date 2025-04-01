from abc import ABC, abstractmethod
from typing import Dict, Tuple


class AbstractUserRepository(ABC):
    @abstractmethod
    def registry_user(self, user_infos: Dict) -> int:
        """Registry user by id"""
        pass

    @abstractmethod
    def find_user_by_id(self, user_id: int) -> Tuple:
        """Find user by ID"""
        pass

    @abstractmethod
    def delete_user_by_id(self, user_id: int) -> None:
        """Delete user by id"""
        pass

    @abstractmethod
    def update_user_by_id(self, new_email: str, user_id: int) -> None:
        """Update user by ID"""
        pass
