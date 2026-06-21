$ErrorActionPreference = "Continue"
$relatorio = New-Object System.Collections.Generic.List[string]
function Log($msg) { Write-Host $msg; $relatorio.Add([string]$msg) }

Log "=========================================="
Log " VERIFICACAO, AUDITORIA E INSTALACAO COMPLETA"
Log " Painel Local - Automacoes Paizante Web AI"
Log "=========================================="
Log ""

# 1) Localizar o hub
$hub = Join-Path $env:USERPROFILE "Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API"
if (-not (Test-Path $hub)) {
    Log "ERRO: hub nao encontrado em $hub"
    Log "Extraia o ZIP do projeto nessa pasta antes de rodar este script."
    Read-Host "Pressione Enter para sair"
    exit 1
}
Log "OK - Hub encontrado em: $hub"
$scripts = Join-Path $hub "05_SCRIPTS_PYTHON"
$painel  = Join-Path $hub "01_PAINEL_LOCAL"

# 2) Verificar Python (instala se ausente ou corrompido)
Log ""
Log "--- [1/7] Python ---"
$pythonOk = $false
try {
    $verPython = (python --version) 2>&1
    $teste = (python -c "import ctypes, encodings; print('OK')") 2>&1
    if ("$teste" -match "OK") {
        $pythonOk = $true
        Log "OK - $verPython funcionando."
    } else {
        Log "FALHA - Python encontrado mas com erro: $teste"
    }
} catch {
    Log "FALHA - Python nao encontrado no PATH."
}

if (-not $pythonOk) {
    Log "Instalando Python 3.12 via winget (precisa de PowerShell como Administrador)..."
    winget install --id Python.Python.3.12 -e --scope machine --silent --accept-package-agreements --accept-source-agreements
    Log "Python instalado. Feche esta janela, abra um PowerShell NOVO e rode este script de novo para continuar."
    Read-Host "Pressione Enter para sair"
    exit 0
}

# 3) Ambiente virtual e dependencias do painel
Log ""
Log "--- [2/7] Ambiente Python do painel (.venv) ---"
Set-Location $scripts
if (-not (Test-Path "$scripts\.venv")) {
    Log "Criando ambiente virtual..."
    python -m venv .venv
}
& "$scripts\.venv\Scripts\python.exe" -m pip install --upgrade pip -q
& "$scripts\.venv\Scripts\python.exe" -m pip install -r "$scripts\requirements.txt" -q
Log "OK - Dependencias instaladas/atualizadas."

# 4) Auditoria: rodar os testes automatizados
Log ""
Log "--- [3/7] Auditoria automatizada (pytest) ---"
$saidaTestes = & "$scripts\.venv\Scripts\python.exe" -m pytest "$scripts\tests" -v 2>&1
$saidaTestes | ForEach-Object { Log $_ }
if ($LASTEXITCODE -eq 0) {
    Log "OK - Todos os testes automatizados passaram."
} else {
    Log "ATENCAO - Pelo menos um teste falhou. Revise as linhas acima."
}

# 5) Google Chrome
Log ""
Log "--- [4/7] Google Chrome ---"
$chromeCaminhos = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)
if ($chromeCaminhos | Where-Object { Test-Path $_ }) {
    Log "OK - Chrome encontrado."
} else {
    Log "Chrome nao encontrado. Instalando via winget..."
    winget install --id Google.Chrome -e --silent --accept-package-agreements --accept-source-agreements
}

# 6) Ollama (IA local gratuita, opcional)
Log ""
Log "--- [5/7] Ollama (IA local opcional) ---"
$ollamaRodando = $false
try {
    Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 3 | Out-Null
    $ollamaRodando = $true
    Log "OK - Ollama ja esta rodando em localhost:11434."
} catch {
    $cmdOllama = Get-Command ollama -ErrorAction SilentlyContinue
    if ($cmdOllama) {
        Log "Ollama instalado mas nao estava rodando. Iniciando..."
        Start-Process "ollama" "serve" -WindowStyle Hidden
        Start-Sleep -Seconds 3
        $ollamaRodando = $true
    } else {
        Log "Ollama nao instalado. Instalando via winget (gratuito, 100% local)..."
        winget install --id Ollama.Ollama -e --silent --accept-package-agreements --accept-source-agreements
        Log "Instalado. Pode ser necessario abrir um PowerShell NOVO para o comando 'ollama' funcionar e baixar os modelos depois."
    }
}

# 7) Modelos recomendados (se Ollama ja disponivel neste terminal)
Log ""
Log "--- [6/7] Modelos de IA local ---"
$cmdOllama = Get-Command ollama -ErrorAction SilentlyContinue
if ($cmdOllama -and $ollamaRodando) {
    $listaModelos = (& ollama list) 2>&1 | Out-String
    if ($listaModelos -notmatch "llama3\.1:8b") {
        Log "Baixando modelo de texto llama3.1:8b (pode levar alguns minutos)..."
        ollama pull llama3.1:8b
    } else {
        Log "OK - llama3.1:8b ja instalado."
    }
} else {
    Log "Ollama ainda nao disponivel neste terminal - pulei o download de modelos. Rode este script de novo depois de instalar."
}

# 8) Atalho na Area de Trabalho
Log ""
Log "--- [7/7] Atalho na Area de Trabalho ---"
$scriptAtalho = Join-Path $painel "criar_atalho_area_trabalho.ps1"
if (Test-Path $scriptAtalho) {
    & $scriptAtalho
} else {
    Log "Script de atalho nao encontrado (pulei esta etapa)."
}

# 9) Relatorio final
$pastaRelatorios = Join-Path $hub "12_RELATORIOS"
New-Item -ItemType Directory -Force -Path $pastaRelatorios | Out-Null
$arquivoRelatorio = Join-Path $pastaRelatorios "verificacao_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
$relatorio -join "`r`n" | Out-File -Encoding utf8 $arquivoRelatorio

Log ""
Log "=========================================="
Log " CONCLUIDO."
Log " Relatorio completo salvo em:"
Log " $arquivoRelatorio"
Log "=========================================="
Read-Host "Pressione Enter para sair"
