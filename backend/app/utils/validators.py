"""
Validadores úteis para o GeoMatch
"""
import re
from typing import Optional


def validate_cep(cep: str) -> bool:
    """
    Valida formato de CEP brasileiro (XXXXX-XXX ou XXXXXXXX)
    
    Args:
        cep: String do CEP a validar
        
    Returns:
        True se válido, False caso contrário
    """
    if not cep:
        return False
    pattern = r'^\d{5}-?\d{3}$'
    return bool(re.match(pattern, cep.strip()))


def extract_cep(text: str) -> Optional[str]:
    """
    Extrai CEP de um texto
    
    Args:
        text: Texto contendo CEP
        
    Returns:
        CEP extraído ou None se não encontrado
    """
    if not text:
        return None
    match = re.search(r'\d{5}-?\d{3}', text)
    return match.group() if match else None


def normalize_cep(cep: str) -> str:
    """
    Normaliza CEP removendo hífen e espaços
    
    Args:
        cep: CEP a normalizar
        
    Returns:
        CEP normalizado (apenas dígitos)
    """
    return re.sub(r'\D', '', cep)


def validate_uf(uf: str) -> bool:
    """
    Valida sigla de UF (Unidade Federativa) brasileira
    
    Args:
        uf: Sigla da UF (2 letras)
        
    Returns:
        True se válido, False caso contrário
    """
    if not uf or len(uf) != 2:
        return False
        
    valid_ufs = [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    ]
    return uf.upper() in valid_ufs


def validate_address_components(address: dict) -> list[str]:
    """
    Valida componentes de um endereço estruturado
    
    Args:
        address: Dicionário com componentes do endereço
        
    Returns:
        Lista de erros encontrados (vazia se válido)
    """
    errors = []
    
    if not address.get('logradouro'):
        errors.append("Logradouro é obrigatório")
        
    if not address.get('cidade'):
        errors.append("Cidade é obrigatória")
        
    if 'uf' in address and not validate_uf(address['uf']):
        errors.append(f"UF inválida: {address.get('uf')}")
        
    if 'cep' in address and not validate_cep(address['cep']):
        errors.append(f"CEP inválido: {address.get('cep')}")
        
    return errors
