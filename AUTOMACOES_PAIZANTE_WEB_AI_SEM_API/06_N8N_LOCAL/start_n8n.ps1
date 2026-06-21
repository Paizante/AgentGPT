$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Arquivo .env criado a partir de .env.example. Edite a senha antes de uso em producao."
}

try {
    docker compose up -d
    Write-Host "n8n local iniciado. Acesse http://localhost:5678"
} catch {
    Write-Host "Nao foi possivel iniciar o n8n via Docker. Verifique se o Docker Desktop esta instalado e rodando."
    Write-Host "Erro: $_"
}
