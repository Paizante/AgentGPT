$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot
try {
    docker compose down
    Write-Host "n8n local parado."
} catch {
    Write-Host "Nao foi possivel parar o n8n via Docker. Verifique se o Docker esta instalado."
}
