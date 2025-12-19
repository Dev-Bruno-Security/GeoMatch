# GeoMatch Backend

FastAPI backend for address normalization, validation/matching with provider failover, scoring, persistence, import/export, and webhook integration for n8n.

## Setup

1. Create and activate a Python environment.
2. Copy `.env.example` to `.env` and adjust settings.
3. Install dependencies and run.

### Windows (PowerShell)

```powershell
cd backend
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API

- `POST /api/upload/csv`: multipart CSV with `address` column (or `endereco`, `logradouro`, `rua`).
- `POST /api/upload/sql`: upload `.sql` contendo inserts; extrai textos de endereços e processa.
- `GET /api/export/csv`: download CSV results.
- `GET /api/export/sql`: download SQL insert dump.
- `GET /api/addresses`: lista endereços normalizados e resultados por provedor.
- `GET /api/addresses/{id}`: obtém um endereço específico.
- `POST /api/webhook/process`: `{ "addresses": ["..."] }` for n8n.
- `GET /api/health`: health check.

## Notes

- Default DB is SQLite in the project folder; set `DATABASE_URL` for PostgreSQL.
- Providers are pluggable via `API_PROVIDERS` env.
- Logging and simple audit via `audit_logs` table.
- Examples: see folder `backend/examples` with `addresses.csv` and `addresses.sql`.
