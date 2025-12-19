# 📮 Feature: Análise de CEP para Matching de Endereços

## Visão Geral

Implementação da extração e utilização de CEP (Código de Endereçamento Postal) como critério adicional para melhorar a precisão da comparação e validação de endereços.

## ✨ Funcionalidades Implementadas

### 1. **Extração Automática de CEP**
- O sistema agora extrai automaticamente CEPs presentes nos endereços de entrada
- Suporta formatos: `12345-678` e `12345678`
- CEPs são normalizados (apenas dígitos) para comparação

### 2. **Armazenamento de CEP**
- Novo campo `cep` na tabela `Address` (CEP do endereço de entrada)
- Novo campo `cep` na tabela `ProviderResult` (CEP retornado pelos provedores)
- CEPs são indexados para consultas rápidas

### 3. **Matching Melhorado com CEP**
- Nova função `similarity_score_with_cep()` que:
  - Calcula score base de similaridade do endereço
  - **Aumenta o score em até 15 pontos** quando ambos CEPs existem e são iguais
  - Quanto menor o score base, maior o boost aplicado
  - Score nunca ultrapassa 100%

**Exemplo:**
```python
# Endereço com score base de 75%
# Se CEPs são iguais: score final = 75 + (15 * 0.25) = 78.75%

# Endereço com score base de 60%
# Se CEPs são iguais: score final = 60 + (15 * 0.40) = 66%
```

### 4. **Visualização no Frontend**
- Nova coluna **"CEP"** mostra o CEP extraído do endereço original
- Nova coluna **"CEP Validado"** mostra o CEP retornado pelo provider
- **Indicador visual (✓)** quando CEPs coincidem (fundo verde)
- CEPs diferentes aparecem em amarelo
- Contador de CEPs encontrados no rodapé da tabela

## 🎯 Benefícios

### 1. **Maior Precisão**
- CEPs idênticos aumentam a confiança no match mesmo com endereços ligeiramente diferentes
- Exemplo: "R. Paulista 100" vs "Av. Paulista 100" com mesmo CEP

### 2. **Validação Cruzada**
- Detecta inconsistências quando endereço parece correto mas CEP diverge
- Útil para identificar endereços incorretos ou desatualizados

### 3. **Melhor UX**
- Usuários podem rapidamente identificar matches com CEP confirmado
- Facilitação na tomada de decisão sobre qual resultado confiar

## 📊 Impacto nas Classificações

O CEP pode melhorar a classificação de matches:

| Score Original | CEPs Iguais? | Score Ajustado | Classificação |
|----------------|--------------|----------------|---------------|
| 75% | Não | 75% | MATCH_POSSIVEL |
| 75% | Sim | ~79% | MATCH_PROVAVEL |
| 85% | Sim | ~88% | MATCH_PROVAVEL |
| 88% | Sim | ~90% | MATCH_CONFIRMADO |

## 🔧 Arquivos Modificados

### Backend
- `app/models.py` - Adicionadas colunas `cep`
- `app/schemas.py` - Adicionados campos `cep`
- `app/services/matching.py` - Nova função `similarity_score_with_cep()`
- `app/routers/upload.py` - Extração e uso de CEP no processamento
- `app/routers/addresses.py` - Inclusão de CEP nos resultados
- `app/utils/validators.py` - Funções já existentes de CEP utilizadas

### Frontend
- `src/components/ResultsTable.jsx` - Novas colunas e indicadores visuais

### Exemplos
- `backend/examples/addresses.csv` - Atualizado com exemplos contendo CEP

## 🧪 Testando a Feature

1. **Com CEP no endereço:**
   ```csv
   address
   Av. Paulista, 1000, São Paulo, SP, 01310-100
   Rua XV de Novembro, 50, Curitiba, PR, 80020-310
   ```

2. **Sem CEP no endereço:**
   ```csv
   address
   Rua da Consolação, 1234, São Paulo
   ```

3. **Observe na tabela:**
   - CEP extraído na coluna "CEP"
   - CEP do provider na coluna "CEP Validado"
   - ✓ verde quando coincidem
   - Score ajustado quando CEPs coincidem

## 🚀 Próximos Passos (Sugestões)

1. **Validação de CEP via ViaCEP**
   - Verificar se CEP existe antes de usar
   - Obter dados adicionais do CEP (bairro, cidade)

2. **Pesos Configuráveis**
   - Permitir ajustar o boost de CEP (atualmente fixo em 15)
   - Configurar por tipo de provider ou regra de negócio

3. **Estatísticas de CEP**
   - Dashboard mostrando % de endereços com CEP
   - Taxa de match de CEPs por provider

4. **Correção de CEP**
   - Sugerir CEP correto quando houver divergência
   - Highlight visual para CEPs inválidos

## 📝 Notas Técnicas

- CEPs são armazenados sem formatação (8 dígitos)
- Formatação visual usa máscara `12345-678`
- Função `extract_cep()` usa regex: `\d{5}-?\d{3}`
- Boost máximo de 15 pontos garante que CEP não sobrepõe totalmente a similaridade textual
- Algoritmo de boost: `boost = 15 * (1 - base_score / 100)`
