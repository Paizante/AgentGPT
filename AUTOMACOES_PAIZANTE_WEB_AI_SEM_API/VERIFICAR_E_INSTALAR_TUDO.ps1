$ErrorActionPreference = "Continue"
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force -ErrorAction SilentlyContinue
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

# 1.1) Aplicar automaticamente pacotes de atualizacao (ZIP) encontrados em Downloads
Log ""
Log "--- [0/8] Pacotes de atualizacao em Downloads ---"
$pastaDownloads = Join-Path $env:USERPROFILE "Downloads"
$zipsAtualizacao = Get-ChildItem -Path $pastaDownloads -Filter "ATUALIZACAO_*.zip" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending
if ($zipsAtualizacao) {
    foreach ($zip in $zipsAtualizacao) {
        Log "Aplicando pacote de atualizacao: $($zip.Name)"
        try {
            Expand-Archive -Path $zip.FullName -DestinationPath (Join-Path $env:USERPROFILE "Documents") -Force
            Log "OK - Pacote $($zip.Name) extraido por cima da pasta do projeto."
        } catch {
            Log "FALHA ao extrair $($zip.Name): $_"
        }
    }
} else {
    Log "Nenhum pacote de atualizacao (ATUALIZACAO_*.zip) encontrado em Downloads. Pulei esta etapa."
}

# 2) Verificar Python (instala se ausente ou corrompido)
Log ""
Log "--- [1/8] Python ---"
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
Log "--- [2/8] Ambiente Python do painel (.venv) ---"
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
Log "--- [3/8] Auditoria automatizada (pytest) ---"
$saidaTestes = & "$scripts\.venv\Scripts\python.exe" -m pytest "$scripts\tests" -v 2>&1
$saidaTestes | ForEach-Object { Log $_ }
if ($LASTEXITCODE -eq 0) {
    Log "OK - Todos os testes automatizados passaram."
} else {
    Log "ATENCAO - Pelo menos um teste falhou. Revise as linhas acima."
}

# 4.1) Verificar se a atualizacao do Chat com IA local (anexos/Ollama) esta presente
Log ""
Log "--- [4/8] Atualizacao do Chat com IA local ---"
$arquivosChat = @(
    (Join-Path $scripts "src\ollama_client.py"),
    (Join-Path $scripts "src\anexo_manager.py"),
    (Join-Path $scripts "src\chat_manager.py"),
    (Join-Path $painel "templates\chat.html")
)
$faltandoChat = $arquivosChat | Where-Object { -not (Test-Path $_) }
if ($faltandoChat.Count -eq 0) {
    Log "OK - Funcionalidade de Chat com IA local (anexos, imagens) esta instalada."
} else {
    Log "ATENCAO - A atualizacao do Chat com IA local NAO esta instalada nesta pasta."
    Log "Arquivos faltando:"
    $faltandoChat | ForEach-Object { Log "  - $_" }
    Log "Para instalar, extraia o pacote de atualizacao (ZIP do chat) por cima desta pasta do projeto e rode este script de novo."
}

# 5) Google Chrome
Log ""
Log "--- [5/8] Google Chrome ---"
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
Log "--- [6/8] Ollama (IA local opcional) ---"
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
Log "--- [7/8] Modelos de IA local ---"
$cmdOllama = Get-Command ollama -ErrorAction SilentlyContinue
if ($cmdOllama -and $ollamaRodando) {
    $listaModelos = (& ollama list) 2>&1 | Out-String
    if ($listaModelos -notmatch "llama3\.1:8b") {
        Log "Baixando modelo de texto llama3.1:8b (pode levar alguns minutos)..."
        $saidaPull = (& ollama pull llama3.1:8b) 2>&1 | Out-String
        Log $saidaPull
        if ($saidaPull -match "i/o timeout|dial tcp|connection refused") {
            Log "FALHA DE REDE ao baixar o modelo. Rodando diagnostico de rede completo..."

            Log ""
            Log "  > Teste de conectividade HTTPS (porta 443) em varios destinos:"
            $destinosTeste = @("registry.ollama.ai", "github.com", "www.google.com")
            $blocked = @{}
            foreach ($destino in $destinosTeste) {
                $r = Test-NetConnection $destino -Port 443 -WarningAction SilentlyContinue
                $blocked[$destino] = -not $r.TcpTestSucceeded
                Log "    - $destino : $(if ($r.TcpTestSucceeded) { 'OK' } else { 'BLOQUEADO' })"
            }

            Log ""
            Log "  > Configuracao de proxy do Windows:"
            $proxy = (netsh winhttp show proxy) 2>&1 | Out-String
            Log "    $proxy".Trim()

            Log ""
            Log "  > Antivirus detectado no sistema:"
            try {
                $avs = Get-CimInstance -Namespace "root/SecurityCenter2" -ClassName AntiVirusProduct -ErrorAction Stop
                if ($avs) { $avs | ForEach-Object { Log "    - $($_.displayName)" } }
                else { Log "    Nenhum antivirus de terceiros detectado (so o Windows Defender padrao)." }
            } catch {
                Log "    Nao foi possivel consultar antivirus instalados nesta sessao."
            }

            Log ""
            if ($blocked["github.com"] -or $blocked["www.google.com"]) {
                Log "DIAGNOSTICO: o bloqueio nao e especifico do Ollama - outros sites HTTPS tambem falharam."
                Log "Isso indica problema geral de rede/firewall/antivirus, nao algo so do registry.ollama.ai."
            } elseif ($blocked["registry.ollama.ai"]) {
                Log "DIAGNOSTICO: apenas registry.ollama.ai esta bloqueado (github.com e google.com funcionaram)."
                Log "Isso indica um bloqueio especifico por dominio/IP - tipico de antivirus com filtro web, controle parental ou firewall corporativo com lista de bloqueio."
            } else {
                Log "DIAGNOSTICO: a porta 443 respondeu neste teste - pode ter sido uma falha temporaria. Tente rodar este script de novo."
            }
            Log "Para confirmar 100% se e bloqueio do roteador/provedor (e nao do Windows), conecte o notebook no Wi-Fi/hotspot do celular e rode este script de novo."
        }
    } else {
        Log "OK - llama3.1:8b ja instalado."
    }
} else {
    Log "Ollama ainda nao disponivel neste terminal - pulei o download de modelos. Rode este script de novo depois de instalar."
}

# 8) Atalho na Area de Trabalho
Log ""
Log "--- [8/8] Atalho na Area de Trabalho ---"
$scriptAtalho = Join-Path $painel "criar_atalho_area_trabalho.ps1"
if (Test-Path $scriptAtalho) {
    $saidaAtalho = (powershell -NoProfile -ExecutionPolicy Bypass -File $scriptAtalho) 2>&1 | Out-String
    Log $saidaAtalho
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
