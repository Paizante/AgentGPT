$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot
try {
    docker compose logs -f --tail=200
} catch {
    Write-Host "Nao foi possivel obter logs do n8n via Docker."
}
