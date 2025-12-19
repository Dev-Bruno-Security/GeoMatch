# 📚 Documentação da API - GeoMatch

## Base URL

```
http://localhost:8000
```

---

## 📤 Upload de Endereços

### Upload CSV

**Endpoint:** `POST /api/upload/csv`

**Descrição:** Faz upload e processa endereços a partir de um arquivo CSV.

**Headers:**
```http
Content-Type: multipart/form-data
```

**Body:**
- `file`: Arquivo CSV (campo multipart/form-data)

**Formato CSV esperado:**
```csv
original_address
Rua José Silva, 123, São Paulo - SP, 01310-100
Av. Paulista, 1000, São Paulo - SP
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "raw_address": "Rua José Silva, 123, São Paulo - SP, 01310-100",
    "normalized_address": "rua jose silva 123 sao paulo sp 01310100",
    "status": "processed",
    "winner_provider": "viacep",
    "results": [
      {
        "provider_name": "viacep",
        "matched_address": "Av. Paulista, Bela Vista, São Paulo, SP",
        "score": 95.5,
        "classification": "MATCH_CONFIRMADO",
        "metadata": {
          "source": "viacep",
          "cep": "01310100"
        }
      }
    ]
  }
]
```

---

### Upload SQL

**Endpoint:** `POST /api/upload/sql`

**Descrição:** Faz upload e processa endereços a partir de um arquivo SQL.

**Headers:**
```http
Content-Type: multipart/form-data
```

**Body:**
- `file`: Arquivo SQL (campo multipart/form-data)

**Formato SQL esperado:**
```sql
INSERT INTO addresses (original_address) VALUES 
('Rua José Silva, 123, São Paulo - SP, 01310-100'),
('Av. Paulista, 1000, São Paulo - SP');
```

**Response:** Mesmo formato do endpoint CSV.

---

## 📋 Consulta de Endereços

### Listar Todos os Endereços

**Endpoint:** `GET /api/addresses`

**Descrição:** Retorna todos os endereços processados.

**Query Parameters:**
- `skip` (opcional): Número de registros para pular (default: 0)
- `limit` (opcional): Número máximo de registros (default: 100, max: 1000)

**Exemplo:**
```http
GET /api/addresses?skip=0&limit=50
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "raw_address": "...",
    "normalized_address": "...",
    "status": "processed",
    "winner_provider": "viacep",
    "results": [...]
  }
]
```

---

### Obter Endereço por ID

**Endpoint:** `GET /api/addresses/{id}`

**Descrição:** Retorna detalhes de um endereço específico.

**Path Parameters:**
- `id`: ID do endereço

**Exemplo:**
```http
GET /api/addresses/1
```

**Response (200 OK):**
```json
{
  "id": 1,
  "raw_address": "Rua José Silva, 123, São Paulo - SP, 01310-100",
  "normalized_address": "rua jose silva 123 sao paulo sp 01310100",
  "status": "processed",
  "winner_provider": "viacep",
  "results": [
    {
      "provider_name": "viacep",
      "matched_address": "Av. Paulista, Bela Vista, São Paulo, SP",
      "score": 95.5,
      "classification": "MATCH_CONFIRMADO",
      "metadata": {
        "source": "viacep",
        "cep": "01310100",
        "logradouro": "Avenida Paulista",
        "bairro": "Bela Vista",
        "localidade": "São Paulo",
        "uf": "SP"
      }
    }
  ]
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Address not found"
}
```

---

## 📥 Exportação

### Exportar CSV

**Endpoint:** `GET /api/export/csv`

**Descrição:** Exporta todos os endereços processados em formato CSV.

**Response (200 OK):**
```
Content-Type: text/csv
Content-Disposition: attachment; filename=addresses_export.csv

id,raw_address,normalized_address,status,winner_provider,winner_score
1,"Rua José Silva, 123","rua jose silva 123",processed,viacep,95.5
```

---

### Exportar SQL

**Endpoint:** `GET /api/export/sql`

**Descrição:** Exporta todos os endereços processados como instruções SQL INSERT.

**Response (200 OK):**
```
Content-Type: text/plain
Content-Disposition: attachment; filename=addresses_export.sql

INSERT INTO addresses (id, raw_address, normalized_address, status, winner_provider, winner_score) VALUES
(1, 'Rua José Silva, 123', 'rua jose silva 123', 'processed', 'viacep', 95.5);
```

---

## 🔄 Webhook

### Processar Endereço via Webhook

**Endpoint:** `POST /api/webhook/process`

**Descrição:** Recebe um endereço via webhook e processa assincronamente.

**Headers:**
```http
Content-Type: application/json
```

**Body:**
```json
{
  "address": "Rua José Silva, 123, São Paulo - SP, 01310-100"
}
```

**Response (200 OK):**
```json
{
  "message": "Address received and queued for processing",
  "address": "Rua José Silva, 123, São Paulo - SP, 01310-100"
}
```

---

## 🏥 Utilidades

### Health Check

**Endpoint:** `GET /api/health`

**Descrição:** Verifica o status da API.

**Response (200 OK):**
```json
{
  "status": "ok",
  "timestamp": "2025-12-18T10:30:00Z",
  "version": "1.0.0"
}
```

---

## 🔐 Códigos de Status

| Código | Descrição |
|--------|-----------|
| 200 | Requisição bem-sucedida |
| 400 | Erro de validação nos dados enviados |
| 404 | Recurso não encontrado |
| 422 | Erro de validação do Pydantic |
| 500 | Erro interno do servidor |

---

## 📊 Classificações de Score

| Classificação | Range | Descrição |
|--------------|-------|-----------|
| MATCH_CONFIRMADO | ≥ 90% | Alta confiança na correspondência |
| MATCH_PROVAVEL | 70-89% | Boa correspondência |
| MATCH_POSSIVEL | 70-79% | Correspondência moderada |
| MATCH_INDEFINIDO | 50-69% | Baixa confiança |
| NO_MATCH | < 50% | Sem correspondência válida |

---

## 🌐 CORS

A API aceita requisições de:
- `http://localhost:5173` (Frontend Vite padrão)
- `http://localhost:3000` (React alternativo)

Configure em `backend/.env`:
```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 🔧 Provedores Disponíveis

### ViaCEP (Padrão)
- **Nome:** `viacep`
- **Requer:** CEP no endereço
- **API:** https://viacep.com.br
- **Timeout:** 5 segundos

### Local
- **Nome:** `local`
- **Fonte:** Banco de dados interno
- **Offline:** Sim

### Dummy
- **Nome:** `dummy`
- **Descrição:** Simulação para testes
- **Sempre retorna:** Match simulado

---

## 📝 Exemplos com cURL

### Upload CSV
```bash
curl -X POST "http://localhost:8000/api/upload/csv" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@addresses.csv"
```

### Listar Endereços
```bash
curl -X GET "http://localhost:8000/api/addresses?limit=10"
```

### Obter Endereço por ID
```bash
curl -X GET "http://localhost:8000/api/addresses/1"
```

### Webhook
```bash
curl -X POST "http://localhost:8000/api/webhook/process" \
  -H "Content-Type: application/json" \
  -d '{"address": "Rua José Silva, 123"}'
```

### Exportar CSV
```bash
curl -X GET "http://localhost:8000/api/export/csv" -o addresses.csv
```

---

## 🔍 Documentação Interativa

Acesse a documentação interativa (Swagger UI):
```
http://localhost:8000/docs
```

Ou a documentação alternativa (ReDoc):
```
http://localhost:8000/redoc
```

---

## 💡 Dicas

1. **Batch Processing:** Use upload CSV/SQL para processar múltiplos endereços de uma vez
2. **Retry Logic:** Configure timeout adequado para APIs externas
3. **Rate Limiting:** ViaCEP tem limite de requisições, use com moderação
4. **Caching:** Considere cachear resultados do ViaCEP para endereços repetidos
5. **Validation:** Sempre valide CEPs antes de enviar para a API

---

**📚 Para mais detalhes, acesse:** http://localhost:8000/docs
