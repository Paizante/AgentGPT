$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot
try {
    docker compose ps
} catch {
    Write-Host "Nao foi possivel consultar o status do n8n via Docker."
}
