from .base import Provider
from ..services.matching import normalize_address


class LocalProvider(Provider):
    name = "local"

    def validate(self, address: str):
        norm = normalize_address(address)
        return {
            "matched_address": norm,
            "score": 100.0,
            "metadata": {"source": "local"},
        }
