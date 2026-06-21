# Abre, em sequencia, o painel local e as tres IAs web - util para iniciar
# um trabalho juridico completo de uma vez. Nenhuma aba e preenchida
# automaticamente; cada envio continua sendo manual.
. (Join-Path $PSScriptRoot "_common.ps1")
Open-UrlsInChrome -Urls @(
    "http://localhost:8000",
    "https://chatgpt.com",
    "https://claude.ai",
    "https://gemini.google.com"
) -NomeFluxo "Fluxo Juridico Completo"
