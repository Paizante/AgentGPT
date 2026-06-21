# Comandos Principais

Pasta principal (deteccao automatica, sem nome de usuario fixo):

```
$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API
```

Todos os comandos abaixo assumem essa pasta como referencia. Substitua
o `cd` pelo caminho real se voce instalou em outro lugar.

## Setup inicial do ambiente Python (rodar uma unica vez)

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\05_SCRIPTS_PYTHON"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Se a ExecutionPolicy bloquear a ativacao da venv, rode uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Rodar os testes automatizados

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\05_SCRIPTS_PYTHON"
.\.venv\Scripts\Activate.ps1
pytest tests\ -v
```

## Abrir o painel local (FastAPI, recomendado para o dia a dia)

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\01_PAINEL_LOCAL"
.\run_painel.ps1
```

Acesse depois em `http://localhost:8000`. O script cria a venv e
instala as dependencias automaticamente na primeira vez, se ainda nao
existirem.

## Abrir o menu de linha de comando (alternativa ao painel)

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\05_SCRIPTS_PYTHON"
.\.venv\Scripts\Activate.ps1
python run.py
```

## Abrir as IAs no Chrome

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\02_CHROME_WORKSPACE"

# todas de uma vez
.\abrir_todas_ias.ps1

# ou individualmente
.\abrir_chatgpt.ps1
.\abrir_claude.ps1
.\abrir_gemini.ps1
.\abrir_n8n.ps1
.\abrir_painel.ps1
.\abrir_fluxo_juridico.ps1
```

## n8n local (opcional, requer Docker Desktop)

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\06_N8N_LOCAL"

.\start_n8n.ps1      # sobe o container (cria .env a partir de .env.example se faltar)
.\status_n8n.ps1     # mostra se esta rodando
.\logs_n8n.ps1       # acompanha os logs em tempo real
.\restart_n8n.ps1    # reinicia
.\stop_n8n.ps1        # para o container
.\backup_n8n.ps1     # faz backup do volume de dados em 10_BACKUPS\n8n
```

Acesse depois em `http://localhost:5678` (usuario/senha definidos no
`.env`, copiado de `.env.example` - troque a senha padrao antes de
usar).

## Ollama local (opcional, 100% gratuito, sem API paga)

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\09_OLLAMA_LOCAL"
.\testar_ollama.ps1
```

## Diagnostico do ambiente

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\12_RELATORIOS"
.\diagnostico.ps1
```

Atualiza `12_RELATORIOS\diagnostico.md` com o estado real da sua
maquina (Windows, PowerShell, Chrome, Python, Docker, Ollama, portas,
espaco em disco etc.), registrando qualquer ferramenta ausente como
pendencia, sem travar a execucao.
