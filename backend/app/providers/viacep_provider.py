"""
Provider real que integra com a API do ViaCEP
"""
import requests
from typing import Dict, Any

from .base import Provider
from ..services.matching import normalize_address, similarity_score
from ..utils.validators import extract_cep, normalize_cep


class ViaCepProvider(Provider):
    """
    Provider que valida endereços usando a API do ViaCEP
    """
    name = "viacep"
    
    def __init__(self):
        self.api_url = "https://viacep.com.br/ws/{}/json/"
        self.timeout = 5  # segundos
    
    def validate(self, address: str) -> Dict[str, Any]:
        """
        Valida endereço consultando a API do ViaCEP
        
        Args:
            address: Endereço a validar (deve conter CEP)
            
        Returns:
            Dicionário com matched_address, score e metadata
            
        Raises:
            ValueError: Se CEP não for encontrado ou for inválido
        """
        # Extrai CEP do endereço
        cep = extract_cep(address)
        if not cep:
            raise ValueError("CEP não encontrado no endereço")
        
        # Normaliza CEP (apenas números)
        clean_cep = normalize_cep(cep)
        
        # Consulta API do ViaCEP
        try:
            response = requests.get(
                self.api_url.format(clean_cep),
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            # Verifica se CEP é válido
            if data.get('erro'):
                raise ValueError(f"CEP inválido: {cep}")
            
            # Monta endereço completo do ViaCEP
            matched_parts = []
            if data.get('logradouro'):
                matched_parts.append(data['logradouro'])
            if data.get('bairro'):
                matched_parts.append(data['bairro'])
            if data.get('localidade'):
                matched_parts.append(data['localidade'])
            if data.get('uf'):
                matched_parts.append(data['uf'])
            
            matched_address = ", ".join(matched_parts)
            
            # Calcula similaridade
            norm_input = normalize_address(address)
            norm_matched = normalize_address(matched_address)
            score = similarity_score(norm_input, norm_matched)
            
            return {
                "matched_address": matched_address,
                "score": score,
                "metadata": {
                    "source": "viacep",
                    "cep": clean_cep,
                    "cep_formatted": f"{clean_cep[:5]}-{clean_cep[5:]}",
                    "logradouro": data.get('logradouro', ''),
                    "complemento": data.get('complemento', ''),
                    "bairro": data.get('bairro', ''),
                    "localidade": data.get('localidade', ''),
                    "uf": data.get('uf', ''),
                    "ibge": data.get('ibge', ''),
                    "ddd": data.get('ddd', '')
                }
            }
            
        except requests.exceptions.Timeout:
            raise ValueError(f"Timeout ao consultar ViaCEP para o CEP: {cep}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Erro ao consultar ViaCEP: {str(e)}")
