from .base import Provider
from ..services.matching import normalize_address, similarity_score


class DummyProvider(Provider):
    name = "dummy"

    def validate(self, address: str):
        # Simula um provedor externo retornando um endereço levemente alterado
        norm = normalize_address(address)
        suggestion = norm.replace(" rua ", " r. ")
        score = similarity_score(norm, suggestion)
        return {
            "matched_address": suggestion,
            "score": score,
            "metadata": {"source": "dummy"},
        }
