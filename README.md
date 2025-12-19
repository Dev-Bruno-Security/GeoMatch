# 🌍 GeoMatch

**Sistema de Normalização e Validação de Endereços com Failover Multi-Provedor**

Sistema completo para normalização, validação e correspondência de endereços brasileiros, com suporte a múltiplos provedores de validação (ViaCEP, Local, Dummy) e interface web intuitiva.

## 🚀 Tecnologias

**Backend:**
- FastAPI (Framework web assíncrono)
- SQLAlchemy (ORM para banco de dados)
- SQLite (Banco de dados)
- pandas (Processamento de dados)
- rapidfuzz (Cálculo de similaridade)
- requests (Cliente HTTP)

**Frontend:**
- React 18
- Vite (Build tool)
- CSS moderno com gradientes

## 📋 Pré-requisitos

- Python 3.8+
- Node.js 16+
- PowerShell (Windows)

## ⚡ Início Rápido

### Opção 1: Script Automatizado (Recomendado - Windows)

```powershell
# Na pasta raiz do projeto
.\start.ps1
```

Este script irá:
- ✅ Verificar todas as dependências
- ✅ Instalar pacotes necessários
- ✅ Iniciar backend e frontend automaticamente
- ✅ Abrir o navegador em http://localhost:5173

### Opção 2: Docker (Recomendado - Multiplataforma)

```bash
# Build e iniciar todos os serviços
docker-compose up

# Ou em background
docker-compose up -d
```

A aplicação estará disponível em:
- 🌐 Frontend: http://localhost:5173
- 🔧 Backend: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

Para mais detalhes, veja [DOCKER.md](DOCKER.md)

### Opção 3: Manual

**Backend:**
```powershell
cd backend

# Criar ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```powershell
cd frontend

# Instalar dependências
npm install

# Configurar variável de ambiente
$env:VITE_API_URL = "http://localhost:8000"

# Iniciar aplicação
npm run dev
```

## 🔧 Configuração

### Backend (.env)

Arquivo já criado em `backend/.env`:

```env
DATABASE_URL=sqlite:///./geomatch.db
DEFAULT_PROVIDER=viacep
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
LOG_LEVEL=INFO
```

### Frontend (.env)

Arquivo já criado em `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

## 📊 Funcionalidades

### ✅ Implementadas

- **Upload de Endereços**: CSV e SQL
- **Normalização**: Remoção de acentos, caracteres especiais, padronização
- **📮 Análise de CEP**: Extração automática e uso na validação (Ver [CEP_FEATURE.md](CEP_FEATURE.md))
  - Extrai CEPs dos endereços de entrada e dos provedores
  - Aumenta score de matching quando CEPs coincidem
  - Visualização de CEPs na interface com indicadores visuais
- **Validação Multi-Provedor**:
  - ✅ ViaCEP (API real)
  - ✅ Local (Banco de dados interno)
  - ✅ Dummy (Simulação)
- **Cálculo de Similaridade**: Score 0-100 com classificações
- **Exportação**: CSV e SQL
- **Interface Web**: Upload, visualização e exportação
- **API REST**: Documentação automática (Swagger)
- **Webhook**: Processamento assíncrono

### 🎯 Classificações de Match

| Score | Classificação | Descrição |
|-------|--------------|-----------|
| ≥ 90% | MATCH_CONFIRMADO | Alta confiança |
| 70-89% | MATCH_PROVAVEL | Boa correspondência |
| 70-79% | MATCH_POSSIVEL | Correspondência moderada |
| 50-69% | MATCH_INDEFINIDO | Baixa confiança |
| < 50% | NO_MATCH | Sem correspondência |

## 📚 Endpoints da API

### Upload
- `POST /api/upload/csv` - Upload de arquivo CSV
- `POST /api/upload/sql` - Upload de arquivo SQL

### Consulta
- `GET /api/addresses` - Lista todos os endereços
- `GET /api/addresses/{id}` - Detalhes de um endereço

### Exportação
- `GET /api/export/csv` - Exporta como CSV
- `GET /api/export/sql` - Exporta como SQL INSERT

### Webhook
- `POST /api/webhook/process` - Processa endereços via webhook

### Utilidades
- `GET /api/health` - Status da API
- `GET /docs` - Documentação interativa (Swagger)

## 🧪 Testes

```powershell
cd backend
pytest tests/test_matching.py -v
```

Testes incluem:
- Normalização de endereços
- Cálculo de similaridade
- Classificação de scores
- Validação de CEP e UF

## 📁 Exemplos de Uso

Arquivos de teste disponíveis em `backend/examples/`:

**addresses.csv:**
```csv
address
Avenida Paulista, 1000, Bela Vista, São Paulo, SP, CEP 01310-100
Rua XV de Novembro, 50, Centro, Curitiba, PR, 80020-310
Praia de Botafogo, 300, Botafogo, Rio de Janeiro, RJ - 22250-040
```

**addresses.sql:**
```sql
INSERT INTO addresses (original_address) VALUES 
('Rua José Silva, 123, São Paulo - SP, 01310-100'),
('Av. Paulista, 1000, Bela Vista, São Paulo - SP');
```

## 🔍 URLs Importantes

| Serviço | URL | Descrição |
|---------|-----|-----------|
| 🌐 Frontend | http://localhost:5173 | Interface web |
| 🔧 Backend | http://localhost:8000 | API REST |
| 📚 Docs | http://localhost:8000/docs | Swagger UI |
| 📖 ReDoc | http://localhost:8000/redoc | Documentação alternativa |

## 🏗️ Estrutura do Projeto

```
GeoMatch/
├── backend/
│   ├── app/
│   │   ├── providers/         # Provedores de validação
│   │   │   ├── viacep_provider.py  ✅ Novo!
│   │   │   ├── local_provider.py
│   │   │   └── dummy_provider.py
│   │   ├── services/          # Serviços de negócio
│   │   ├── routers/           # Endpoints da API
│   │   ├── utils/             # Utilitários ✅ Novo!
│   │   │   └── validators.py
│   │   └── main.py
│   ├── tests/                 # Testes ✅ Novo!
│   │   └── test_matching.py
│   └── .env                   # Configurações ✅ Novo!
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ExportButtons.jsx  ✅ Novo!
│   │   │   ├── UploadForm.jsx
│   │   │   └── ResultsTable.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css         # Estilos ✅ Novo!
│   └── .env                   # Configurações ✅ Novo!
└── start.ps1                  # Script de inicialização ✅ Novo!
```

## 🎨 Recursos de UI

- Design moderno com gradientes
- Animações suaves
- Tabelas responsivas
- Badges coloridos por classificação
- Botões de exportação estilizados
- Layout responsivo

## 🛠️ Desenvolvimento

### Adicionar Novo Provider

```python
# backend/app/providers/novo_provider.py
from .base import Provider

class NovoProvider(Provider):
    name = "novo"
    
    def validate(self, address: str):
        # Sua lógica aqui
        return {
            "matched_address": "...",
            "score": 85.0,
            "metadata": {}
        }
```

Registre em `backend/app/providers/__init__.py`:
```python
from .novo_provider import NovoProvider

def get_providers(names: List[str]):
    mapping = {
        "novo": NovoProvider,
        # ...
    }
```

## � Docker

### Quick Start com Docker

```bash
docker-compose up
```

Acesse:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Docs: http://localhost:8000/docs

### Comandos Docker Úteis

```bash
# Build das imagens
docker-compose build

# Iniciar em background
docker-compose up -d

# Ver logs do backend
docker-compose logs backend -f

# Ver logs do frontend
docker-compose logs frontend -f

# Parar os serviços
docker-compose down

# Remover volumes (limpar banco de dados)
docker-compose down -v
```

Para mais detalhes, veja [DOCKER.md](DOCKER.md)

## �📝 Licença

Este é um projeto MVP para demonstração.

## 👥 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique a documentação em http://localhost:8000/docs
2. Revise os logs no console
3. Abra uma issue no repositório

---

**Desenvolvido com ❤️ usando FastAPI e React**
