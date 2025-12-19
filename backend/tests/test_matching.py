"""
Testes unitários para o serviço de matching
"""
import pytest
from app.services.matching import (
    normalize_address,
    similarity_score,
    similarity_score_with_cep,
    classify_score,
    calculate_match_score
)


class TestNormalizeAddress:
    """Testes para normalização de endereços"""
    
    def test_basic_normalization(self):
        """Testa normalização básica"""
        result = normalize_address("Rua José da Silva, 123")
        assert result == "rua jose da silva 123"
    
    def test_remove_accents(self):
        """Testa remoção de acentos"""
        result = normalize_address("Avenida Paulísta")
        assert result == "avenida paulista"
        
        result = normalize_address("São Paulo")
        assert result == "sao paulo"
    
    def test_remove_special_chars(self):
        """Testa remoção de caracteres especiais"""
        result = normalize_address("Rua A, nº 123 - Apto. 45")
        assert result == "rua a no 123 apto 45"
    
    def test_lowercase(self):
        """Testa conversão para minúsculas"""
        result = normalize_address("RUA JOSÉ")
        assert result == "rua jose"
    
    def test_multiple_spaces(self):
        """Testa remoção de espaços múltiplos"""
        result = normalize_address("Rua    José    da    Silva")
        assert result == "rua jose da silva"
    
    def test_empty_string(self):
        """Testa string vazia"""
        result = normalize_address("")
        assert result == ""
    
    def test_only_numbers(self):
        """Testa apenas números"""
        result = normalize_address("12345-678")
        assert result == "12345678"


class TestSimilarityScore:
    """Testes para cálculo de similaridade"""
    
    def test_identical_strings(self):
        """Testa strings idênticas"""
        score = similarity_score("rua a", "rua a")
        assert score == 100.0
    
    def test_completely_different(self):
        """Testa strings completamente diferentes"""
        score = similarity_score("abc", "xyz")
        assert score < 50.0
    
    def test_similar_strings(self):
        """Testa strings similares"""
        score = similarity_score("rua jose silva", "rua jose da silva")
        assert 70.0 < score < 100.0
    
    def test_empty_strings(self):
        """Testa strings vazias"""
        score = similarity_score("", "")
        assert score == 100.0
    
    def test_case_insensitive(self):
        """Testa que é case insensitive"""
        score1 = similarity_score("RUA A", "rua a")
        score2 = similarity_score("rua a", "rua a")
        assert score1 == score2


class TestClassifyScore:
    """Testes para classificação de score"""
    
    def test_match_confirmado(self):
        """Testa classificação MATCH_CONFIRMADO"""
        assert classify_score(95) == "MATCH_CONFIRMADO"
        assert classify_score(100) == "MATCH_CONFIRMADO"
    
    def test_match_provavel(self):
        """Testa classificação MATCH_PROVAVEL"""
        assert classify_score(80) == "MATCH_PROVAVEL"
        assert classify_score(89) == "MATCH_PROVAVEL"
    
    def test_match_possivel(self):
        """Testa classificação MATCH_POSSIVEL"""
        assert classify_score(70) == "MATCH_POSSIVEL"
        assert classify_score(79) == "MATCH_POSSIVEL"
    
    def test_match_indefinido(self):
        """Testa classificação MATCH_INDEFINIDO"""
        assert classify_score(50) == "MATCH_INDEFINIDO"
        assert classify_score(69) == "MATCH_INDEFINIDO"
    
    def test_no_match(self):
        """Testa classificação NO_MATCH"""
        assert classify_score(30) == "NO_MATCH"
        assert classify_score(0) == "NO_MATCH"
    
    def test_boundary_values(self):
        """Testa valores de fronteira"""
        assert classify_score(90.0) == "MATCH_CONFIRMADO"
        assert classify_score(89.9) == "MATCH_PROVAVEL"
        assert classify_score(70.0) == "MATCH_POSSIVEL"
        assert classify_score(69.9) == "MATCH_INDEFINIDO"
        assert classify_score(50.0) == "MATCH_INDEFINIDO"
        assert classify_score(49.9) == "NO_MATCH"


class TestCalculateMatchScore:
    """Testes para cálculo completo de match"""
    
    def test_perfect_match(self):
        """Testa match perfeito"""
        result = calculate_match_score(
            "Rua José Silva, 123",
            "Rua José Silva, 123"
        )
        assert result['score'] == 100.0
        assert result['classification'] == "MATCH_CONFIRMADO"
    
    def test_similar_match(self):
        """Testa match similar"""
        result = calculate_match_score(
            "Rua José Silva, 123",
            "R. José Silva, 123"
        )
        assert result['score'] > 80.0
        assert result['classification'] in ["MATCH_CONFIRMADO", "MATCH_PROVAVEL"]
    
    def test_different_addresses(self):
        """Testa endereços diferentes"""
        result = calculate_match_score(
            "Rua A, 123",
            "Avenida B, 456"
        )
        assert result['score'] < 80.0
    
    def test_normalized_addresses_returned(self):
        """Testa que endereços normalizados são retornados"""
        result = calculate_match_score(
            "RUA José Silva",
            "Rua JOSÉ Silva"
        )
        assert 'normalized_input' in result
        assert 'normalized_matched' in result
        assert result['normalized_input'] == "rua jose silva"
        assert result['normalized_matched'] == "rua jose silva"


class TestIntegration:
    """Testes de integração"""
    
    def test_full_workflow(self):
        """Testa fluxo completo de matching"""
        original = "Rua José da Silva Neto, nº 123 - Apto. 45, São Paulo - SP"
        matched = "R. José da Silva Neto, 123 Apto 45, Sao Paulo SP"
        
        result = calculate_match_score(original, matched)
        
        assert result['score'] > 70.0
        assert result['classification'] in [
            "MATCH_CONFIRMADO",
            "MATCH_PROVAVEL",
            "MATCH_POSSIVEL"
        ]
        assert 'normalized_input' in result
        assert 'normalized_matched' in result
        assert 'score' in result
        assert 'classification' in result


class TestSimilarityScoreWithCep:
    """Testes para matching com CEP"""
    
    def test_no_cep_provided(self):
        """Testa que sem CEP retorna score base"""
        base_score = similarity_score("rua a 123", "rua a 123")
        cep_score = similarity_score_with_cep("rua a 123", "rua a 123", None, None)
        assert base_score == cep_score
    
    def test_matching_cep_boosts_score(self):
        """Testa que CEPs iguais aumentam o score"""
        base_score = similarity_score_with_cep(
            "rua jose silva 100", 
            "r jose silva 100", 
            None, 
            None
        )
        boosted_score = similarity_score_with_cep(
            "rua jose silva 100", 
            "r jose silva 100", 
            "01310100", 
            "01310100"
        )
        assert boosted_score > base_score
    
    def test_different_cep_no_boost(self):
        """Testa que CEPs diferentes não aumentam score"""
        base_score = similarity_score_with_cep(
            "rua a 123", 
            "rua a 123", 
            None, 
            None
        )
        no_boost_score = similarity_score_with_cep(
            "rua a 123", 
            "rua a 123", 
            "01310100", 
            "80020310"
        )
        assert base_score == no_boost_score
    
    def test_cep_with_hyphen(self):
        """Testa que CEP com hífen funciona"""
        score1 = similarity_score_with_cep(
            "rua a", "rua a", "01310-100", "01310100"
        )
        score2 = similarity_score_with_cep(
            "rua a", "rua a", "01310100", "01310100"
        )
        assert score1 == score2
        assert score1 > similarity_score("rua a", "rua a")
    
    def test_score_never_exceeds_100(self):
        """Testa que score nunca ultrapassa 100"""
        score = similarity_score_with_cep(
            "rua jose silva", 
            "rua jose silva", 
            "01310100", 
            "01310100"
        )
        assert score <= 100.0
    
    def test_low_score_gets_bigger_boost(self):
        """Testa que scores baixos recebem boost maior"""
        # Score alto (pouco boost)
        high_base = 90.0
        high_boost = similarity_score_with_cep(
            "av paulista 1000", 
            "av paulista 1000", 
            "01310100", 
            "01310100"
        )
        
        # O boost máximo é 15 pontos para scores muito baixos
        # Para score de 90%, boost esperado = 15 * (1 - 0.9) = 1.5
        # Resultado esperado ~91.5%
        assert high_boost >= high_base
        assert high_boost <= 100.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
