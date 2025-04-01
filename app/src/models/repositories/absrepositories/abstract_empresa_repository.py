from abc import ABC, abstractmethod
from typing import Dict, Tuple


class AbstractEmpresaRepository(ABC):

    @abstractmethod
    def registry_empresa(self, empresa_infos: Dict) -> int:
        """Registry empresa by id"""
        pass

    @abstractmethod
    def find_empresa_by_id(self, empresa_id: int) -> Tuple:
        """Find empresa by ID"""
        pass

    @abstractmethod
    def delete_empresa_by_id(self, empresa_id: int) -> None:
        """Delete empresa by id"""
        pass

    @abstractmethod
    def update_empresa_by_id(self, new_infos: Dict, empresa_id: int) -> None:
        """Update empresa by ID"""
        pass
