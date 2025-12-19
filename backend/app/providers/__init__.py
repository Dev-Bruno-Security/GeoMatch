from typing import List

from .local_provider import LocalProvider
from .dummy_provider import DummyProvider
from .viacep_provider import ViaCepProvider


def get_providers(names: List[str]):
    mapping = {
        "local": LocalProvider,
        "dummy": DummyProvider,
        "viacep": ViaCepProvider,
    }
    providers = []
    for n in names:
        cls = mapping.get(n)
        if cls:
            providers.append(cls())
    return providers
