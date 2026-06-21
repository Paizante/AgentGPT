# Inicia o painel local FastAPI em http://localhost:8000 (somente 127.0.0.1).
$ErrorActionPreference = "Stop"

$PastaPrincipal = Join-Path $env:USERPROFILE "Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API"
$PastaScripts = Join-Path $PastaPrincipal "05_SCRIPTS_PYTHON"
$Venv = Join-Path $PastaScripts ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $PastaScripts)) {
    Write-Host "Pasta de scripts Python nao encontrada em: $PastaScripts"
    exit 1
}

Set-Location $PastaScripts

if (-not (Test-Path $Venv)) {
    Write-Host "Criando ambiente virtual Python (.venv)..."
    python -m venv .venv
    Write-Host "Se houver erro de ExecutionPolicy, rode: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned"
}

. $Venv
pip install -r requirements.txt
Set-Location ..\01_PAINEL_LOCAL
uvicorn app.main:app --host 127.0.0.1 --port 8000
