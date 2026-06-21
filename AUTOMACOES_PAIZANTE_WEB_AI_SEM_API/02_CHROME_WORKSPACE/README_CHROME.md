# Chrome Workspace

Scripts PowerShell que apenas **abrem abas** no Google Chrome para o
painel local e para ChatGPT, Claude e Gemini. Nenhum script desta pasta
preenche login, senha, prompt ou clica em "enviar" - tudo isso continua
sendo feito manualmente pelo usuario.

## Scripts

- `abrir_chatgpt.ps1` - abre https://chatgpt.com
- `abrir_claude.ps1` - abre https://claude.ai
- `abrir_gemini.ps1` - abre https://gemini.google.com
- `abrir_n8n.ps1` - abre http://localhost:5678
- `abrir_painel.ps1` - abre http://localhost:8000
- `abrir_todas_ias.ps1` - abre as 3 IAs de uma vez, cada uma em sua aba
- `abrir_fluxo_juridico.ps1` - abre painel + as 3 IAs de uma vez
- `_common.ps1` - funcoes compartilhadas (deteccao do chrome.exe, log)

## Como usar

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\02_CHROME_WORKSPACE"
.\abrir_todas_ias.ps1
```

Os scripts detectam automaticamente o caminho do `chrome.exe` em locais
comuns de instalacao e no PATH. Se o Chrome nao for encontrado, o script
avisa na tela e grava a falha em `11_LOGS\chrome\chrome.log`, sem
interromper o restante da automacao.
