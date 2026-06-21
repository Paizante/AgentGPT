# Painel Local

Painel web (FastAPI + Jinja2) que roda em http://localhost:8000, com bind
exclusivo em `127.0.0.1` (nao acessivel pela rede/internet).

## Funcionalidades

- Criar trabalho (tipo de tarefa, cliente, resumo do caso, IAs a usar).
- Gerar prompt especifico por IA (ChatGPT, Claude, Gemini).
- Copiar prompt para a area de transferencia.
- Abrir a IA correspondente no Chrome (sem preencher nada automaticamente).
- Registrar confirmacao manual de envio.
- Colar e salvar a resposta de cada IA.
- Comparar respostas, consolidar, gerar versao final e checklist de
  protocolo.
- Abrir a pasta do trabalho/cliente no Explorador de Arquivos.
- Gerar backup do trabalho.

## Tipos de tarefa suportados

Analise juridica, revisao de peca, criacao de peticao, requerimento
administrativo, LOAS/BPC, auxilio-doenca, reclamacao trabalhista, mandado
de seguranca, procuracao, contrato de honorarios, declaracao, organizacao
documental, analise de documentos, prompt para Claude Code, automacao n8n,
edicao de video, relatorio de reuniao, resumo de e-mails, plano de acao e
comparacao entre IAs (ver `src/config.py` -> `TIPOS_TAREFA`).

## Como rodar

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\01_PAINEL_LOCAL"
.\run_painel.ps1
```

Depois abra http://localhost:8000 (ou use
`02_CHROME_WORKSPACE\abrir_painel.ps1`).

## Estrutura

- `app/main.py` - rotas FastAPI.
- `templates/` - paginas HTML (Jinja2).
- `static/` - CSS e JS (copia para clipboard).
- `data/trabalhos/<job_id>/` - pasta canonica de cada trabalho (metadata,
  prompts, respostas, comparativo, consolidado, final, checklist, log).

O painel reaproveita toda a logica de negocio dos modulos em
`05_SCRIPTS_PYTHON/src` (job_manager, prompt_builder, response_collector,
response_comparer, response_consolidator, organizador_clientes,
checklist_protocolo, clipboard_tools, browser_launcher, file_utils).
