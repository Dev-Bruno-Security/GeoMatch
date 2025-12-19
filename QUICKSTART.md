# 🚀 Guia Rápido - GeoMatch

## ⚡ Opções de Inicialização

### Opção 1: Docker (Recomendado - Fácil e Rápido)

**Windows (PowerShell):**
```powershell
.\docker.ps1 up
```

**Linux/Mac:**
```bash
make up
```

**Ou com Docker Compose direto:**
```bash
docker-compose up
```

✅ **Pronto!** Acesse http://localhost:5173

### Opção 2: Script Automatizado (Windows)

```powershell
.\start.ps1
```

### Opção 3: Manual

**Terminal 1 - Backend:**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

---

## 📍 Acessar a Aplicação

| Serviço | URL |
|---------|-----|
| 🌐 Frontend | http://localhost:5173 |
| 🔧 Backend | http://localhost:8000 |
| 📚 Documentação API | http://localhost:8000/docs |

---

## Como Usar

### 1️⃣ Upload de Endereços

**Opção A - CSV:**
```csv
address
Rua José Silva, 123, São Paulo - SP, 01310-100
Av. Paulista, 1000, São Paulo - SP
Avenida Paulista, 1000, Bela Vista, São Paulo, SP, CEP 01310-100
```

**Opção B - SQL:**
```sql
INSERT INTO addresses (raw_address) VALUES 
('Rua José Silva, 123, São Paulo - SP, 01310-100');
```

### 2️⃣ Validação Automática

O sistema irá:
- ✅ Normalizar o endereço
- ✅ Validar com ViaCEP (se houver CEP)
- ✅ Calcular score de similaridade
- ✅ Classificar o resultado

### 3️⃣ Visualizar Resultados

A tabela mostrá:
- Endereço original
- Endereço validado
- Score (0-100)
- Classificação

### 4️⃣ Exportar Dados

Clique em:
- **📥 Exportar CSV** - Para planilhas
- **📥 Exportar SQL** - Para banco de dados

---

## Provedores Disponíveis

### ViaCEP (Padrão)
- Valida CEPs reais
- Retorna endereço completo
- Requer CEP no texto

### Local
- Busca em banco de dados interno
- Mais rápido
- Funciona offline

### Dummy
- Simulação para testes
- Sempre retorna resultado
- Útil para desenvolvimento

---

## Classificações de Score

| Score | Badge | Significado |
|-------|-------|-------------|
| ≥ 90% | 🟢 MATCH_CONFIRMADO | Endereço validado com alta confiança |
| 70-89% | 🟡 MATCH_PROVAVEL | Boa correspondência |
| 70-79% | 🟠 MATCH_POSSIVEL | Correspondência moderada |
| 50-69% | 🔵 MATCH_INDEFINIDO | Baixa confiança |
| < 50% | 🔴 NO_MATCH | Sem correspondência |

---

## Exemplos de Testes

### Teste 1: CEP Válido
```
01310-100
```
✅ ViaCEP encontrará: Av. Paulista, São Paulo - SP

### Teste 2: Endereço Completo
```
Rua José Silva, 123, São Paulo - SP, 01310-100
```
✅ Score alto (>90%)

### Teste 3: Endereço Similar
```
R. José Silva, 123, SP
```
✅ Score médio (70-89%)

---

## Resolução de Problemas

### Backend não inicia
```powershell
# Reinstale as dependências
cd backend
pip install -r requirements.txt --force-reinstall
```

### Frontend não inicia
```powershell
# Reinstale node_modules
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

### Porta em uso
```powershell
# Backend (8000)
netstat -ano | findstr :8000
# Mate o processo com o PID
taskkill /PID <PID> /F

# Frontend (5173)
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### Erro de CORS
Verifique se `backend/.env` tem:
```env
CORS_ORIGINS=http://localhost:5173
```

---

## Atalhos Úteis

| Ação | URL |
|------|-----|
| 🌐 Abrir aplicação | http://localhost:5173 |
| 📚 Ver documentação | http://localhost:8000/docs |
| 🔍 Testar API | http://localhost:8000/docs (Swagger) |
| 📊 Ver banco de dados | Abrir `backend/geomatch.db` com SQLite Browser |

---

## Comandos de Desenvolvimento

### Rodar Testes
```powershell
cd backend
pytest tests/ -v
```

### Limpar Banco de Dados
```powershell
cd backend
Remove-Item geomatch.db
# Reinicie o backend para recriar
```

### Verificar Logs
```powershell
# Backend - veja no terminal onde rodou uvicorn
# ou em backend/logs/geomatch.log
```

---

## Próximos Passos

1. ✅ Configure o provider no `backend/.env`:
   ```env
   DEFAULT_PROVIDER=viacep
   ```

2. ✅ Teste com os arquivos de exemplo:
   - `backend/examples/addresses.csv`
   - `backend/examples/addresses.sql`

3. ✅ Explore a API em: http://localhost:8000/docs

4. ✅ Customize os estilos em: `frontend/src/styles.css`

---

**💡 Dica:** Use o script `start.ps1` para iniciar tudo automaticamente!

**🆘 Problemas?** Verifique os logs no terminal ou console do navegador (F12).
