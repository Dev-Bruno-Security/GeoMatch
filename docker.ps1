# Script para facilitar uso do Docker no GeoMatch
# Uso: .\docker.ps1 [comando]

param(
    [string]$Command = "up"
)

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "🐳 GeoMatch Docker Manager" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se Docker está instalado
$dockerCheck = docker --version 2>$null
if (-not $dockerCheck) {
    Write-Host "❌ Docker não encontrado!" -ForegroundColor Red
    Write-Host "💡 Instale o Docker Desktop em: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Docker encontrado: $dockerCheck" -ForegroundColor Green
Write-Host ""

# Verifica se está na pasta correta
if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "❌ Arquivo docker-compose.yml não encontrado!" -ForegroundColor Red
    Write-Host "💡 Execute este script na pasta raiz do projeto" -ForegroundColor Yellow
    exit 1
}

# Executa comando
switch ($Command.ToLower()) {
    "up" {
        Write-Host "🚀 Iniciando containers..." -ForegroundColor Green
        docker-compose up
    }
    "down" {
        Write-Host "🛑 Parando containers..." -ForegroundColor Yellow
        docker-compose down
    }
    "build" {
        Write-Host "🔨 Reconstruindo imagens..." -ForegroundColor Green
        docker-compose build
    }
    "logs" {
        Write-Host "📋 Mostrando logs..." -ForegroundColor Green
        docker-compose logs -f
    }
    "logs-backend" {
        Write-Host "📋 Logs do backend..." -ForegroundColor Green
        docker-compose logs backend -f
    }
    "logs-frontend" {
        Write-Host "📋 Logs do frontend..." -ForegroundColor Green
        docker-compose logs frontend -f
    }
    "status" {
        Write-Host "📊 Status dos containers:" -ForegroundColor Green
        docker-compose ps
    }
    "clean" {
        Write-Host "🧹 Limpando volumes e containers..." -ForegroundColor Yellow
        docker-compose down -v
        Write-Host "✓ Limpeza concluída" -ForegroundColor Green
    }
    "shell-backend" {
        Write-Host "🔌 Acessando shell do backend..." -ForegroundColor Green
        docker-compose exec backend /bin/bash
    }
    "shell-frontend" {
        Write-Host "🔌 Acessando shell do frontend..." -ForegroundColor Green
        docker-compose exec frontend /bin/sh
    }
    "test" {
        Write-Host "🧪 Executando testes..." -ForegroundColor Green
        docker-compose exec backend python -m pytest tests/test_matching.py -v
    }
    default {
        Write-Host "Comandos disponíveis:" -ForegroundColor Green
        Write-Host ""
        Write-Host "  ./docker.ps1 up              - Iniciar containers"
        Write-Host "  ./docker.ps1 down            - Parar containers"
        Write-Host "  ./docker.ps1 build           - Reconstruir imagens"
        Write-Host "  ./docker.ps1 logs            - Ver todos os logs"
        Write-Host "  ./docker.ps1 logs-backend    - Ver logs do backend"
        Write-Host "  ./docker.ps1 logs-frontend   - Ver logs do frontend"
        Write-Host "  ./docker.ps1 status          - Status dos containers"
        Write-Host "  ./docker.ps1 clean           - Remover containers e volumes"
        Write-Host "  ./docker.ps1 shell-backend   - Acessar shell do backend"
        Write-Host "  ./docker.ps1 shell-frontend  - Acessar shell do frontend"
        Write-Host "  ./docker.ps1 test            - Executar testes"
        Write-Host ""
    }
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "URLs de Acesso:" -ForegroundColor Green
Write-Host "  🌐 Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "  🔧 Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "  📚 Docs:     http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
