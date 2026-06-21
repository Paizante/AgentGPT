# Scripts Python

Codigo Python da central Automacoes Paizante Web AI Sem API. Sem
nenhuma API paga de IA - apenas automacao local (FastAPI, PDF/DOCX,
clipboard, abertura de Chrome, organizacao documental, comparacao e
consolidacao de respostas coladas manualmente).

## Setup

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\05_SCRIPTS_PYTHON"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Se a ExecutionPolicy bloquear a ativacao da venv:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Estrutura

- `run.py` - menu interativo de linha de comando com 20 opcoes.
- `src/config.py` - deteccao da pasta base e configuracao central.
- `src/logger.py` - logging padronizado em `11_LOGS/python`.
- `src/file_utils.py` - utilitarios de arquivo (sempre em copia).
- `src/pdf_tools.py` - unir/separar/extrair texto de PDF.
- `src/docx_tools.py` - leitura/criacao basica de DOCX.
- `src/clipboard_tools.py` - copiar prompts para a area de transferencia.
- `src/browser_launcher.py` - abrir ChatGPT/Claude/Gemini/painel/n8n no Chrome.
- `src/prompt_builder.py` - geracao de prompts especificos por IA.
- `src/prompt_splitter.py` - divisao de textos longos em partes.
- `src/job_manager.py` - criacao e gestao dos trabalhos (jobs).
- `src/response_collector.py` - coleta de respostas coladas manualmente.
- `src/response_comparer.py` - comparacao entre respostas das IAs.
- `src/response_consolidator.py` - consolidacao e versao final.
- `src/organizador_clientes.py` - pastas e organizacao por cliente.
- `src/renomeador_documentos.py` - renomeacao padronizada de copias.
- `src/relatorio_documental.py` - indice documental do cliente.
- `src/checklist_protocolo.py` - checklist de protocolo.
- `src/main_menu.py` - menu interativo usado por `run.py`.
- `tests/` - testes automatizados (pytest).

## Testes

```powershell
pytest
```
