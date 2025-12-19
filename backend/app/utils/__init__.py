"""
Arquivo __init__.py para o pacote utils
"""
from .validators import (
    validate_cep,
    extract_cep,
    normalize_cep,
    validate_uf,
    validate_address_components
)

__all__ = [
    'validate_cep',
    'extract_cep',
    'normalize_cep',
    'validate_uf',
    'validate_address_components'
]
