$ErrorActionPreference = "Continue"
$PastaPrincipal = Join-Path $env:USERPROFILE "Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API"
$DestinoBackup = Join-Path $PastaPrincipal "10_BACKUPS\n8n"
$Selo = Get-Date -Format "yyyyMMdd_HHmmss"

try {
    if (-not (Test-Path $DestinoBackup)) { New-Item -ItemType Directory -Path $DestinoBackup -Force | Out-Null }
    docker run --rm -v paizante_n8n_data:/data -v "${DestinoBackup}:/backup" alpine `
        tar czf "/backup/n8n_data_$Selo.tar.gz" -C /data .
    Write-Host "Backup do volume n8n salvo em $DestinoBackup\n8n_data_$Selo.tar.gz"
} catch {
    Write-Host "Nao foi possivel gerar backup do volume n8n via Docker. Verifique se o Docker esta rodando."
}
