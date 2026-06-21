# Relatorio de Instalacao

## O que foi gerado

A pasta `AUTOMACOES_PAIZANTE_WEB_AI_SEM_API` foi criada/gerada com a
estrutura completa das 13 areas numeradas (00 a 12), totalizando os
arquivos descritos em `12_RELATORIOS/mapa_da_estrutura.md`.

## Onde instalar no seu computador

1. Copie (ou clone) a pasta inteira `AUTOMACOES_PAIZANTE_WEB_AI_SEM_API`
   para dentro de `$env:USERPROFILE\Documents\` no Windows, de modo que o
   caminho final seja:

   ```
   $env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API
   ```

   Todos os scripts detectam essa pasta automaticamente a partir da
   propria localizacao do arquivo (nunca assumem um nome fixo de usuario
   como "gusta").

## Python (painel local + scripts)

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\05_SCRIPTS_PYTHON"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Se o PowerShell bloquear a ativacao da venv com erro de
ExecutionPolicy, rode uma vez (como o proprio usuario, sem precisar de
administrador):

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Instalado e testado neste ambiente de geracao: todas as 17 dependencias
de `requirements.txt` (fastapi, uvicorn, jinja2, python-multipart,
pypdf, pymupdf, python-docx, pandas, openpyxl, rich, typer, pydantic,
python-dotenv, pyyaml, pyperclip, watchdog, pytest) foram instaladas
sem erro. Ver `12_RELATORIOS/testes.md` para o resultado dos testes.

## n8n local (opcional, requer Docker Desktop)

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\06_N8N_LOCAL"
.\start_n8n.ps1
```

O `docker-compose.yml` foi validado sintaticamente (`docker compose
config`) neste ambiente de geracao e esta correto: bind exclusivo em
`127.0.0.1:5678`, volume nomeado `paizante_n8n_data` para persistencia
e autenticacao basica habilitada por padrao. A subida real do
container (`docker compose up -d`) depende do Docker Desktop estar
instalado e rodando no Windows do usuario - isso e uma pendencia de
ambiente, nao de codigo.

## Ollama local (opcional)

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\09_OLLAMA_LOCAL"
.\testar_ollama.ps1
```

Se o Ollama nao estiver instalado, o script registra a pendencia e
informa onde baixar (https://ollama.com), sem travar o restante do
fluxo - o Ollama e 100% opcional neste hub.

## Painel local (FastAPI)

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\01_PAINEL_LOCAL"
.\run_painel.ps1
```

Abre em `http://localhost:8000`, somente em loopback (nunca exposto na
rede).

## Chrome (abertura manual das IAs)

Os scripts em `02_CHROME_WORKSPACE` detectam o Chrome instalado
automaticamente (ou caem para o navegador padrao do sistema via
`webbrowser`, no caso dos scripts Python equivalentes). Nenhum script
preenche login, cola texto ou clica em enviar - tudo isso e sempre
manual.

## Pendencias de instalacao

Ver lista completa e priorizada em `12_RELATORIOS/pendencias.md`.
