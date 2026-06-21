$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot
try {
    docker compose restart
    Write-Host "n8n local reiniciado."
} catch {
    Write-Host "Nao foi possivel reiniciar o n8n via Docker."
}
