.PHONY: help build up down logs logs-backend logs-frontend status clean shell-backend shell-frontend test restart

help:
	@echo "🐳 GeoMatch Docker Commands"
	@echo ""
	@echo "  make build              - Reconstruir imagens Docker"
	@echo "  make up                 - Iniciar containers"
	@echo "  make down               - Parar containers"
	@echo "  make restart            - Reiniciar containers"
	@echo "  make logs               - Ver todos os logs"
	@echo "  make logs-backend       - Ver logs do backend"
	@echo "  make logs-frontend      - Ver logs do frontend"
	@echo "  make status             - Status dos containers"
	@echo "  make clean              - Remover containers e volumes"
	@echo "  make shell-backend      - Acessar shell do backend"
	@echo "  make shell-frontend     - Acessar shell do frontend"
	@echo "  make test               - Executar testes"
	@echo ""
	@echo "URLs de Acesso:"
	@echo "  🌐 Frontend: http://localhost:5173"
	@echo "  🔧 Backend:  http://localhost:8000"
	@echo "  📚 Docs:     http://localhost:8000/docs"

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

restart: down up

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs backend -f

logs-frontend:
	docker-compose logs frontend -f

status:
	docker-compose ps

clean:
	docker-compose down -v

shell-backend:
	docker-compose exec backend /bin/bash

shell-frontend:
	docker-compose exec frontend /bin/sh

test:
	docker-compose exec backend python -m pytest tests/test_matching.py -v

.DEFAULT_GOAL := help
