$ErrorActionPreference = "Continue"
Write-Host "Testando Ollama local em http://localhost:11434 ..."

try {
    $resposta = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 5
    Write-Host "Ollama esta rodando. Modelos instalados:"
    if ($resposta.models) {
        $resposta.models | ForEach-Object { Write-Host "- $($_.name)" }
    } else {
        Write-Host "(nenhum modelo instalado ainda - use: ollama pull llama3.1:8b)"
    }
} catch {
    Write-Host "Ollama nao respondeu em localhost:11434."
    Write-Host "Verifique se esta instalado e rodando (icone do Ollama ou: ollama serve)."
    Write-Host "Instalacao: https://ollama.com/download (gratuito, sem API paga)."
}
