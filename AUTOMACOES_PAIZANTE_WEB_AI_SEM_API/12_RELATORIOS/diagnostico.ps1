# ============================================================================
# diagnostico.ps1
# Diagnostico do ambiente Windows para AUTOMACOES_PAIZANTE_WEB_AI_SEM_API
# Execute este script no PowerShell do Windows real do usuario.
# Nunca falha: cada verificacao usa try/catch e qualquer ausencia
# se torna uma PENDENCIA registrada, nunca um erro que interrompe a execucao.
# ============================================================================

$ErrorActionPreference = "Continue"

$Pasta = Join-Path $env:USERPROFILE "Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API"
$RelatorioPath = Join-Path $Pasta "12_RELATORIOS\diagnostico.md"
$Pendencias = @()
$Linhas = @()

function Add-Linha($texto) { $script:Linhas += $texto }
function Add-Pendencia($texto) { $script:Pendencias += $texto }

Add-Linha "# Diagnostico do Ambiente"
Add-Linha ""
Add-Linha "Gerado em: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Add-Linha ""
Add-Linha "## Usuario e pastas"
Add-Linha ""

try { Add-Linha "- Usuario Windows: $env:USERNAME" } catch { Add-Pendencia "Nao foi possivel ler USERNAME" }
try { Add-Linha "- USERPROFILE: $env:USERPROFILE" } catch { Add-Pendencia "Nao foi possivel ler USERPROFILE" }
try { Add-Linha "- Pasta Documents detectada: $(Join-Path $env:USERPROFILE 'Documents')" } catch { Add-Pendencia "Nao foi possivel detectar pasta Documents" }
try { Add-Linha "- Pasta principal do projeto: $Pasta" } catch { Add-Pendencia "Nao foi possivel montar caminho da pasta principal" }

Add-Linha ""
Add-Linha "## Sistema"
Add-Linha ""

try {
    $os = Get-CimInstance Win32_OperatingSystem -ErrorAction Stop
    Add-Linha "- Windows: $($os.Caption) (build $($os.BuildNumber))"
} catch {
    Add-Pendencia "Nao foi possivel obter versao do Windows (Get-CimInstance falhou)."
}

try {
    $psv = $PSVersionTable.PSVersion.ToString()
    Add-Linha "- PowerShell: $psv"
} catch {
    Add-Pendencia "Nao foi possivel obter versao do PowerShell."
}

try {
    $policy = Get-ExecutionPolicy
    Add-Linha "- Execution Policy atual: $policy"
    if ($policy -eq "Restricted") {
        Add-Pendencia "ExecutionPolicy = Restricted. Rode: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned"
    }
} catch {
    Add-Pendencia "Nao foi possivel ler a ExecutionPolicy."
}

Add-Linha ""
Add-Linha "## Ferramentas"
Add-Linha ""

$ferramentas = @(
    @{ Nome = "Chrome"; Cmd = { Get-ChildItem -Path @(
            "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
            "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
            "$env:LocalAppData\Google\Chrome\Application\chrome.exe"
        ) -ErrorAction Stop | Select-Object -First 1 -ExpandProperty FullName } },
    @{ Nome = "Python"; Cmd = { (python --version) 2>&1 } },
    @{ Nome = "pip"; Cmd = { (pip --version) 2>&1 } },
    @{ Nome = "Git"; Cmd = { (git --version) 2>&1 } },
    @{ Nome = "Node"; Cmd = { (node --version) 2>&1 } },
    @{ Nome = "npm"; Cmd = { (npm --version) 2>&1 } },
    @{ Nome = "Docker"; Cmd = { (docker --version) 2>&1 } },
    @{ Nome = "Docker Compose"; Cmd = { (docker compose version) 2>&1 } },
    @{ Nome = "Ollama"; Cmd = { (ollama --version) 2>&1 } },
    @{ Nome = "Tailscale"; Cmd = { (tailscale version) 2>&1 } }
)

foreach ($f in $ferramentas) {
    try {
        $resultado = & $f.Cmd
        if ($resultado) {
            Add-Linha "- $($f.Nome): OK -> $resultado"
        } else {
            Add-Linha "- $($f.Nome): nao encontrado"
            Add-Pendencia "$($f.Nome) nao encontrado no PATH."
        }
    } catch {
        Add-Linha "- $($f.Nome): nao encontrado"
        Add-Pendencia "$($f.Nome) nao encontrado ou comando falhou."
    }
}

Add-Linha ""
Add-Linha "## Portas locais"
Add-Linha ""

foreach ($porta in 5678, 8000, 11434) {
    try {
        $teste = Test-NetConnection -ComputerName "127.0.0.1" -Port $porta -WarningAction SilentlyContinue -ErrorAction Stop
        if ($teste.TcpTestSucceeded) {
            Add-Linha "- Porta $porta : EM USO (algo ja esta escutando)"
        } else {
            Add-Linha "- Porta $porta : livre"
        }
    } catch {
        Add-Linha "- Porta $porta : nao foi possivel testar"
        Add-Pendencia "Nao foi possivel testar a porta $porta."
    }
}

Add-Linha ""
Add-Linha "## Disco e permissoes"
Add-Linha ""

try {
    $drive = (Get-PSDrive -Name ($env:USERPROFILE.Substring(0,1)) -ErrorAction Stop)
    $livreGB = [math]::Round($drive.Free / 1GB, 2)
    Add-Linha "- Espaco livre no disco do usuario: $livreGB GB"
} catch {
    Add-Pendencia "Nao foi possivel medir espaco em disco."
}

try {
    if (-not (Test-Path $Pasta)) { New-Item -ItemType Directory -Path $Pasta -Force | Out-Null }
    $testFile = Join-Path $Pasta "12_RELATORIOS\_teste_escrita.tmp"
    "teste" | Out-File -FilePath $testFile -Encoding utf8 -Force
    Remove-Item $testFile -Force
    Add-Linha "- Permissao de escrita na pasta principal: OK"
} catch {
    Add-Linha "- Permissao de escrita na pasta principal: FALHOU"
    Add-Pendencia "Sem permissao de escrita em $Pasta."
}

Add-Linha ""
Add-Linha "## Container/volume n8n antigo"
Add-Linha ""

try {
    $cont = docker ps -a --filter "name=n8n" --format "{{.Names}} | {{.Status}}" 2>&1
    if ($cont) {
        Add-Linha "- Containers n8n encontrados: $cont"
    } else {
        Add-Linha "- Nenhum container n8n encontrado."
    }
} catch {
    Add-Linha "- Nao foi possivel consultar containers n8n (Docker pode estar ausente)."
}

try {
    $vol = docker volume ls --filter "name=n8n" --format "{{.Name}}" 2>&1
    if ($vol) {
        Add-Linha "- Volumes n8n encontrados: $vol"
    } else {
        Add-Linha "- Nenhum volume n8n encontrado."
    }
} catch {
    Add-Linha "- Nao foi possivel consultar volumes n8n (Docker pode estar ausente)."
}

Add-Linha ""
Add-Linha "## Pendencias registradas"
Add-Linha ""

if ($Pendencias.Count -eq 0) {
    Add-Linha "Nenhuma pendencia detectada."
} else {
    foreach ($p in $Pendencias) { Add-Linha "- [ ] $p" }
}

try {
    $dirRel = Split-Path $RelatorioPath -Parent
    if (-not (Test-Path $dirRel)) { New-Item -ItemType Directory -Path $dirRel -Force | Out-Null }
    $Linhas -join "`r`n" | Out-File -FilePath $RelatorioPath -Encoding utf8 -Force
    Write-Host "Diagnostico salvo em: $RelatorioPath"
} catch {
    Write-Host "Nao foi possivel salvar o relatorio em $RelatorioPath. Exibindo no console:"
    $Linhas | ForEach-Object { Write-Host $_ }
}
