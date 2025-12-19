# Script para iniciar o GeoMatch (Backend + Frontend)
# Uso: .\start.ps1

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "🚀 Iniciando GeoMatch..." -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se está na pasta raiz do projeto
if (-not (Test-Path "backend\app\main.py")) {
    Write-Host "❌ Erro: Execute este script na pasta raiz do projeto GeoMatch!" -ForegroundColor Red
    exit 1
}

# Define o diretório base
$baseDir = Get-Location

# Função para verificar se uma porta está em uso
function Test-Port {
    param($Port)
    $connection = Test-NetConnection -ComputerName localhost -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue
    return $connection
}

# Verifica se as portas estão disponíveis
Write-Host "🔍 Verificando portas..." -ForegroundColor Yellow
if (Test-Port 8000) {
    Write-Host "⚠️  Porta 8000 já está em uso!" -ForegroundColor Yellow
}
if (Test-Port 5173) {
    Write-Host "⚠️  Porta 5173 já está em uso!" -ForegroundColor Yellow
}
Write-Host ""

# Verifica ambiente virtual Python (aceita backend\.venv ou raiz \.venv)
Write-Host "🐍 Verificando ambiente Python..." -ForegroundColor Yellow
$venvActivatePath = $null
if (Test-Path "backend\.venv\Scripts\Activate.ps1") {
    $venvActivatePath = "$baseDir\backend\.venv\Scripts\Activate.ps1"
} elseif (Test-Path "\.venv\Scripts\Activate.ps1") {
    $venvActivatePath = "$baseDir\.venv\Scripts\Activate.ps1"
}
if (-not $venvActivatePath) {
    Write-Host "❌ Ambiente virtual Python não encontrado!" -ForegroundColor Red
    Write-Host "💡 Execute: python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r backend/requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Verifica node_modules
Write-Host "📦 Verificando dependências Node.js..." -ForegroundColor Yellow
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "⚠️  Node modules não encontrados. Instalando..." -ForegroundColor Yellow
    Set-Location "frontend"
    npm install
    Set-Location $baseDir
}
Write-Host ""

# Inicia o Backend
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "🔧 Iniciando Backend (FastAPI)..." -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan

Start-Process powershell -ArgumentList `
    "-NoExit", `
    "-Command", `
    "cd '$baseDir\backend'; " + `
    "& '$venvActivatePath'; " + `
    "Write-Host '🔧 Backend rodando em http://localhost:8000' -ForegroundColor Green; " + `
    "Write-Host '📚 Documentação: http://localhost:8000/docs' -ForegroundColor Cyan; " + `
    "Write-Host '' ; " + `
    "uvicorn app.main:app --reload --port 8000"

# Aguarda o backend iniciar
Write-Host "⏳ Aguardando backend inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Testa se o backend iniciou
$backendReady = $false
for ($i = 0; $i -lt 10; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/" -Method GET -TimeoutSec 2 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            $backendReady = $true
            break
        }
    } catch {
        Start-Sleep -Seconds 2
    }
}

if ($backendReady) {
    Write-Host "✅ Backend iniciado com sucesso!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Backend pode estar demorando para iniciar..." -ForegroundColor Yellow
}
Write-Host ""

# Inicia o Frontend
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "⚛️  Iniciando Frontend (React + Vite)..." -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan

Start-Process powershell -ArgumentList `
    "-NoExit", `
    "-Command", `
    "cd '$baseDir\frontend'; " + `
    "`$env:VITE_API_URL='http://localhost:8000'; " + `
    "Write-Host '⚛️  Frontend rodando em http://localhost:5173' -ForegroundColor Green; " + `
    "Write-Host '' ; " + `
    "npm run dev"

# Aguarda o frontend iniciar
Write-Host "⏳ Aguardando frontend inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
Write-Host ""

# Resumo
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "✅ GeoMatch Iniciado!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 URLs Importantes:" -ForegroundColor White
Write-Host "   🌐 Frontend:      http://localhost:5173" -ForegroundColor Cyan
Write-Host "   🔧 Backend:       http://localhost:8000" -ForegroundColor Cyan
Write-Host "   📚 Documentação:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Para parar os serviços, feche as janelas do PowerShell." -ForegroundColor Yellow
Write-Host ""
Write-Host "🎯 Acesse http://localhost:5173 para começar a usar!" -ForegroundColor Green
Write-Host ""

# Abre o navegador automaticamente
Start-Sleep -Seconds 2
Write-Host "🌐 Abrindo navegador..." -ForegroundColor Yellow
Start-Process "http://localhost:5173"
