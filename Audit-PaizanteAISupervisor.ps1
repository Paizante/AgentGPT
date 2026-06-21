<#
Auditoria somente-leitura do ambiente para o projeto Paizante AI Supervisor V3.
Nao instala, nao apaga, nao altera nada. Apenas coleta e imprime o estado atual,
e grava um relatorio em texto para consulta posterior.

Uso:
    powershell -ExecutionPolicy Bypass -File Audit-PaizanteAISupervisor.ps1
#>

$ErrorActionPreference = 'SilentlyContinue'
$ReportDir  = Join-Path $env:USERPROFILE 'Documents\PaizanteAISupervisor\LOGS'
$Timestamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$ReportPath = Join-Path $ReportDir "audit_$Timestamp.txt"

if (-not (Test-Path $ReportDir)) {
    New-Item -ItemType Directory -Path $ReportDir -Force | Out-Null
}

$lines = New-Object System.Collections.Generic.List[string]
function Add-Line([string]$text) {
    $lines.Add($text)
    Write-Host $text
}
function Add-Section([string]$title) {
    Add-Line ''
    Add-Line ('=' * 70)
    Add-Line $title
    Add-Line ('=' * 70)
}

Add-Line "Auditoria Paizante AI Supervisor V3 - $(Get-Date)"
Add-Line "Usuario: $env:USERNAME  Maquina: $env:COMPUTERNAME"

# ---------------------------------------------------------------------------
Add-Section 'HARDWARE E SISTEMA'
try {
    $os  = Get-CimInstance Win32_OperatingSystem
    $cpu = Get-CimInstance Win32_Processor
    $gpu = Get-CimInstance Win32_VideoController | Where-Object { $_.Name -match 'NVIDIA|Intel' }
    Add-Line "SO: $($os.Caption) (Build $($os.BuildNumber))"
    Add-Line "CPU: $($cpu.Name)"
    Add-Line ("RAM total: {0:N1} GB / RAM livre: {1:N1} GB" -f ($os.TotalVisibleMemorySize/1MB), ($os.FreePhysicalMemory/1MB))
    foreach ($g in $gpu) {
        Add-Line "GPU: $($g.Name) - VRAM aprox: $([math]::Round($g.AdapterRAM/1GB,1)) GB"
    }
    $drive = Get-PSDrive -Name C
    Add-Line ("Disco C: livre {0:N1} GB de {1:N1} GB" -f ($drive.Free/1GB), (($drive.Used+$drive.Free)/1GB))
} catch { Add-Line "Falha ao coletar dados de hardware: $_" }

# ---------------------------------------------------------------------------
Add-Section 'GPU NVIDIA (nvidia-smi)'
$nvidiaSmi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
if ($nvidiaSmi) {
    Add-Line (& nvidia-smi --query-gpu=name,memory.total,memory.used,temperature.gpu,utilization.gpu --format=csv)
} else {
    Add-Line "nvidia-smi nao encontrado no PATH."
}

# ---------------------------------------------------------------------------
Add-Section 'FERRAMENTAS DE LINHA DE COMANDO (PATH)'
$tools = @('python','python3','node','npm','npx','git','ffmpeg','ollama','codex','claude','codex-paizante','claude-paizante','pwsh','powershell')
foreach ($t in $tools) {
    $cmd = Get-Command $t -ErrorAction SilentlyContinue
    if ($cmd) {
        $verOutput = $null
        try { $verOutput = & $cmd.Source --version 2>$null | Select-Object -First 1 } catch {}
        Add-Line "[OK]    $t -> $($cmd.Source)  $verOutput"
    } else {
        Add-Line "[AUSENTE] $t"
    }
}

# ---------------------------------------------------------------------------
Add-Section 'OLLAMA'
$ollamaCmd = Get-Command ollama -ErrorAction SilentlyContinue
if ($ollamaCmd) {
    Add-Line "ollama list:"
    Add-Line (& ollama list 2>&1 | Out-String)
    try {
        $resp = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -Method Get -TimeoutSec 5
        Add-Line "Endpoint local respondeu OK. Modelos via API:"
        $resp.models | ForEach-Object { Add-Line " - $($_.name)  ($([math]::Round($_.size/1GB,2)) GB)" }
    } catch {
        Add-Line "Endpoint http://127.0.0.1:11434 nao respondeu (servico pode estar parado). $_"
    }
} else {
    Add-Line "Comando 'ollama' nao encontrado no PATH."
}

# ---------------------------------------------------------------------------
Add-Section 'APLICATIVOS (Store / instalados)'
$appKeywords = @('ChatGPT','Codex','Claude','OpenAI')
try {
    $appxList = Get-AppxPackage | Where-Object { $appKeywords -contains ($_.Name -replace '.*\.','') -or ($appKeywords | Where-Object { $_ -and $_ -ne '' } | ForEach-Object { $_ } | Where-Object { $true }) }
} catch {}
foreach ($kw in $appKeywords) {
    $pkgs = Get-AppxPackage | Where-Object { $_.Name -match $kw }
    foreach ($p in $pkgs) {
        Add-Line "Appx: $($p.Name)  Version: $($p.Version)  Install: $($p.InstallLocation)"
    }
}
Add-Line ""
Add-Line "Get-StartApps (filtrado):"
try {
    Get-StartApps | Where-Object { $_.Name -match 'ChatGPT|Codex|Claude' } | ForEach-Object {
        Add-Line " - $($_.Name)  AppID: $($_.AppID)"
    }
} catch { Add-Line "Get-StartApps indisponivel." }

# ---------------------------------------------------------------------------
Add-Section 'CHROME'
$chromePaths = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)
$chromeFound = $chromePaths | Where-Object { Test-Path $_ }
if ($chromeFound) {
    foreach ($c in $chromeFound) { Add-Line "Chrome encontrado: $c" }
} else {
    Add-Line "Chrome nao encontrado nos caminhos padrao."
}

# ---------------------------------------------------------------------------
Add-Section 'DIRETORIOS RELACIONADOS AO PROJETO'
$dirsToCheck = @(
    "$env:LOCALAPPDATA\PaizanteVisionAgent",
    "$env:LOCALAPPDATA\PaizanteLocalAgent",
    "$env:LOCALAPPDATA\PaizanteAISupervisor",
    "$env:USERPROFILE\Documents\PaizanteAISupervisor",
    "$env:APPDATA\ui-tars-desktop",
    "$env:APPDATA\Claude",
    "$env:USERPROFILE\Downloads"
)
foreach ($d in $dirsToCheck) {
    if (Test-Path $d) {
        $itemCount = (Get-ChildItem -Path $d -ErrorAction SilentlyContinue | Measure-Object).Count
        $size = (Get-ChildItem -Path $d -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        $sizeStr = if ($size) { "{0:N1} MB" -f ($size/1MB) } else { "0 MB" }
        Add-Line "[EXISTE] $d  ($itemCount itens, $sizeStr)"
    } else {
        Add-Line "[NAO EXISTE] $d"
    }
}

# ---------------------------------------------------------------------------
Add-Section 'VERSOES ANTERIORES (V1/V2/V2.1/V2.2/V2.3) E SCRIPTS EM DOWNLOADS'
$downloads = "$env:USERPROFILE\Downloads"
if (Test-Path $downloads) {
    $candidates = Get-ChildItem -Path $downloads -Recurse -Include '*paizante*','*Paizante*' -ErrorAction SilentlyContinue
    if ($candidates) {
        $candidates | ForEach-Object { Add-Line " - $($_.FullName)  ($($_.LastWriteTime))" }
    } else {
        Add-Line "Nenhum arquivo com 'paizante' no nome encontrado em Downloads."
    }
}

# ---------------------------------------------------------------------------
Add-Section 'CODEX CLI E CLAUDE CODE - DETALHE'
foreach ($pair in @(@{cmd='codex'; pkg='@openai/codex'}, @{cmd='claude'; pkg='@anthropic-ai/claude-code'})) {
    $c = Get-Command $pair.cmd -ErrorAction SilentlyContinue
    if ($c) {
        Add-Line "$($pair.cmd) encontrado em: $($c.Source)"
        try { Add-Line ("  Versao: " + (& $c.Source --version 2>&1 | Select-Object -First 1)) } catch {}
    } else {
        Add-Line "$($pair.cmd) NAO encontrado no PATH (pacote oficial: $($pair.pkg))"
    }
}
$npmGlobal = Get-Command npm -ErrorAction SilentlyContinue
if ($npmGlobal) {
    Add-Line ""
    Add-Line "Pacotes npm globais instalados:"
    Add-Line (& npm list -g --depth=0 2>&1 | Out-String)
}

# ---------------------------------------------------------------------------
Add-Section 'RESUMO'
Add-Line "Relatorio salvo em: $ReportPath"
Add-Line "Revise antes de instalar qualquer novo componente, para evitar duplicidade."

$lines -join "`r`n" | Out-File -FilePath $ReportPath -Encoding UTF8
Write-Host ""
Write-Host "Relatorio completo gravado em: $ReportPath" -ForegroundColor Green
