import re
import unicodedata
from rapidfuzz import fuzz
from typing import Optional


def normalize_address(addr: str) -> str:
    s = addr.lower().strip()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    # remove hyphens without adding spaces (e.g., 12345-678 -> 12345678)
    s = s.replace("-", "")
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def similarity_score(a: str, b: str) -> float:
    # ensure case-insensitive comparison
    return float(fuzz.token_sort_ratio(a.lower(), b.lower()))


def similarity_score_with_cep(a: str, b: str, cep_a: Optional[str] = None, cep_b: Optional[str] = None) -> float:
    """
    Calcula score de similaridade considerando CEP.
    Se ambos CEPs existirem e forem iguais, aumenta o score base.
    
    Args:
        a: Primeiro endereço
        b: Segundo endereço
        cep_a: CEP do primeiro endereço (opcional)
        cep_b: CEP do segundo endereço (opcional)
        
    Returns:
        Score de similaridade ajustado (0-100)
    """
    base_score = similarity_score(a, b)
    
    # Se ambos CEPs existem e são iguais, aumenta o score
    if cep_a and cep_b:
        # Normaliza CEPs para comparação
        clean_cep_a = re.sub(r'\D', '', cep_a)
        clean_cep_b = re.sub(r'\D', '', cep_b)
        
        if clean_cep_a == clean_cep_b:
            # CEPs iguais: aumenta o score em até 15 pontos
            # Quanto menor o score base, maior o boost
            boost = 15 * (1 - base_score / 100)
            return min(100.0, base_score + boost)
    
    return base_score


def pick_best_result(results):
    if not results:
        return None
    return max(results, key=lambda r: r["score"])


def classify_score(score: float) -> str:
    # thresholds aligned with tests and docs
    if score >= 90:
        return "MATCH_CONFIRMADO"
    if score >= 80:
        return "MATCH_PROVAVEL"
    if score >= 70:
        return "MATCH_POSSIVEL"
    if score >= 50:
        return "MATCH_INDEFINIDO"
    return "NO_MATCH"


def calculate_match_score(input_addr: str, matched_addr: str) -> dict:
    """Calcula score de similaridade entre enderecos normalizados e retorna classificacao.

    Retorna dicionario com normalized_input, normalized_matched, score e classification.
    """
    norm_input = normalize_address(input_addr)
    norm_matched = normalize_address(matched_addr)
    score = similarity_score(norm_input, norm_matched)
    return {
        "normalized_input": norm_input,
        "normalized_matched": norm_matched,
        "score": score,
        "classification": classify_score(score),
    }
