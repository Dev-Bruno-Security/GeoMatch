from abc import ABC, abstractmethod
from typing import Dict, Any


class Provider(ABC):
    name: str

    @abstractmethod
    def validate(self, address: str) -> Dict[str, Any]:
        """Valida/corresponde um endereço. Retorna dict com matched_address, score, metadata."""
        raise NotImplementedError
