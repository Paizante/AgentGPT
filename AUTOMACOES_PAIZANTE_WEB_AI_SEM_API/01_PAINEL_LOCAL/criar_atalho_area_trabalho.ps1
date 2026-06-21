# Cria um atalho "Painel Paizante" na Area de Trabalho do usuario, apontando
# para ABRIR_PAINEL_PAIZANTE.bat. Roda uma unica vez. Modo "criar, nunca
# destruir": se o atalho ja existir, nada e sobrescrito.
$ErrorActionPreference = "Stop"

$PainelDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CaminhoBat = Join-Path $PainelDir "ABRIR_PAINEL_PAIZANTE.bat"
$AreaTrabalho = [Environment]::GetFolderPath("Desktop")
$CaminhoAtalho = Join-Path $AreaTrabalho "Painel Paizante.lnk"

if (-not (Test-Path $CaminhoBat)) {
    Write-Host "Nao encontrei ABRIR_PAINEL_PAIZANTE.bat em $PainelDir"
    exit 1
}

if (Test-Path $CaminhoAtalho) {
    Write-Host "Ja existe um atalho em: $CaminhoAtalho"
    Write-Host "Nada foi sobrescrito (modo 'criar, nunca destruir')."
    exit 0
}

$WshShell = New-Object -ComObject WScript.Shell
$Atalho = $WshShell.CreateShortcut($CaminhoAtalho)
$Atalho.TargetPath = $CaminhoBat
$Atalho.WorkingDirectory = $PainelDir
$Atalho.IconLocation = "shell32.dll,220"
$Atalho.Description = "Abre o Painel Local Automacoes Paizante (http://localhost:8000)"
$Atalho.Save()

Write-Host "Atalho criado com sucesso em: $CaminhoAtalho"
Write-Host "A partir de agora, basta dar dois cliques nele na Area de Trabalho."
