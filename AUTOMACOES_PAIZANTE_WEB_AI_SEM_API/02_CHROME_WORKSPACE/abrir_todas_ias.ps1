. (Join-Path $PSScriptRoot "_common.ps1")
Open-UrlsInChrome -Urls @(
    "https://chatgpt.com",
    "https://claude.ai",
    "https://gemini.google.com"
) -NomeFluxo "Todas as IAs"
