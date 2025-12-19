# 🐳 Guia Docker - GeoMatch

## Pré-requisitos

- Docker Desktop instalado e rodando
- Docker Compose (geralmente incluído com Docker Desktop)

## Início Rápido com Docker

### 1. Build das imagens (primeiro uso)

```bash
docker-compose build
```

### 2. Iniciar os serviços

```bash
docker-compose up
```

Ou em background:

```bash
docker-compose up -d
```

### 3. Acessar a aplicação

- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8000
- **Documentação API:** http://localhost:8000/docs

### 4. Parar os serviços

```bash
docker-compose down
```

## Comandos Úteis

### Ver logs do backend
```bash
docker-compose logs backend -f
```

### Ver logs do frontend
```bash
docker-compose logs frontend -f
```

### Executar comando no backend
```bash
docker-compose exec backend python -m pytest tests/test_matching.py -v
```

### Acessar shell do backend
```bash
docker-compose exec backend /bin/bash
```

### Acessar shell do frontend
```bash
docker-compose exec frontend /bin/sh
```

### Reconstruir sem cache
```bash
docker-compose build --no-cache
```

### Remover containers, redes e volumes
```bash
docker-compose down -v
```

## Variáveis de Ambiente

### Backend
Edite o `docker-compose.yml` ou crie um arquivo `.env`:

```env
DATABASE_URL=sqlite:///./geomatch.db
DEFAULT_PROVIDER=viacep
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
LOG_LEVEL=INFO
```

### Frontend
Configure em `docker-compose.yml`:

```yaml
environment:
  - VITE_API_URL=http://backend:8000
```

## Troubleshooting

### Porta já está em uso

Se a porta 5173 ou 8000 já estiver em uso, mude no `docker-compose.yml`:

```yaml
ports:
  - "5174:5173"  # Frontend em 5174
  - "8001:8000"  # Backend em 8001
```

### Backend não responde

Verifique os logs:
```bash
docker-compose logs backend
```

### Database locked

Remova o arquivo de banco e reinicie:
```bash
docker-compose down -v
docker-compose up
```

### Reconstruir uma imagem específica

```bash
docker-compose build backend --no-cache
docker-compose up backend
```

## Volumes e Persistência

O banco de dados SQLite é salvo em volume e persiste entre containers:

```yaml
volumes:
  - ./backend/geomatch.db:/app/geomatch.db
```

Para limpar completamente:
```bash
docker-compose down -v
```

## Performance

- **Multi-stage builds:** As imagens usam multi-stage para reduzir o tamanho
- **Alpine Linux:** Frontend usa `node:20-alpine` para tamanho mínimo
- **Health checks:** Ambos os serviços têm health checks configurados

## Desenvolvimento com Docker

Para desenvolvimento com hot-reload, você pode:

1. Manter o backend rodando no Docker
2. Rodar o frontend localmente:

```bash
# Terminal 1
docker-compose up backend

# Terminal 2
cd frontend
npm install
npm run dev
```

## Produção

Para produção, você pode:

1. Usar as imagens Docker existentes
2. Adicionar um reverse proxy (nginx)
3. Usar um orquestrador (Kubernetes)
4. Adicionar SSL/TLS
5. Configurar logging centralizado

Exemplo com Nginx será adicionado em breve.
