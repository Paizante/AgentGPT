# Funcoes comuns para os scripts do Chrome Workspace.
# NUNCA preenche login/senha, nunca clica em "enviar", nunca le cookies/sessao/token.

function Find-ChromePath {
    $candidatos = @(
        "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
        "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
        "$env:LocalAppData\Google\Chrome\Application\chrome.exe"
    )
    foreach ($c in $candidatos) {
        if (Test-Path $c) { return $c }
    }
    try {
        $cmd = Get-Command chrome.exe -ErrorAction Stop
        return $cmd.Source
    } catch {
        return $null
    }
}

function Get-PastaPrincipal {
    return Join-Path $env:USERPROFILE "Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API"
}

function Write-LogChrome($mensagem) {
    $pasta = Join-Path (Get-PastaPrincipal) "11_LOGS\chrome"
    try {
        if (-not (Test-Path $pasta)) { New-Item -ItemType Directory -Path $pasta -Force | Out-Null }
        $linha = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $mensagem"
        Add-Content -Path (Join-Path $pasta "chrome.log") -Value $linha
    } catch {
        Write-Host "Aviso: nao foi possivel gravar log em $pasta"
    }
}

function Open-UrlsInChrome {
    param(
        [string[]]$Urls,
        [string]$NomeFluxo
    )
    $chrome = Find-ChromePath
    if (-not $chrome) {
        Write-Host "Chrome nao encontrado neste computador. Instale o Google Chrome e tente novamente."
        Write-LogChrome "FALHA - Chrome nao encontrado ao tentar abrir [$NomeFluxo]: $($Urls -join ', ')"
        return
    }
    foreach ($url in $Urls) {
        Start-Process -FilePath $chrome -ArgumentList $url
        Write-LogChrome "OK - Aba aberta [$NomeFluxo]: $url"
    }
    Write-Host "Abertas $($Urls.Count) aba(s) para [$NomeFluxo]. Login e envio sao sempre manuais."
}
