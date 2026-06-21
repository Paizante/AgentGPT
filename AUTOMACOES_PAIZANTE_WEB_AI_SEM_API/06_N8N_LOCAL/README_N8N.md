# n8n Local

n8n Community Edition rodando 100% local via Docker Compose, sem VPS,
sem dominio e sem porta exposta para a internet (bind exclusivo em
`127.0.0.1:5678`).

## Scripts

- `start_n8n.ps1` - sobe o n8n (`docker compose up -d`).
- `stop_n8n.ps1` - para o n8n.
- `restart_n8n.ps1` - reinicia o n8n.
- `logs_n8n.ps1` - mostra os logs em tempo real.
- `status_n8n.ps1` - mostra o status do container.
- `backup_n8n.ps1` - gera backup do volume `paizante_n8n_data` em
  `10_BACKUPS/n8n`.

## Primeiro uso

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\06_N8N_LOCAL"
.\start_n8n.ps1
```

Acesse http://localhost:5678 (usuario/senha definidos em `.env`, copiado
automaticamente de `.env.example` no primeiro start - troque a senha
padrao).

## Workflows de exemplo

Pasta `workflows/`: `novo_trabalho.json`, `checklist_documental.json`,
`rotina_backup.json`, `registrar_resposta_ia.json`,
`gerar_relatorio_diario.json`, `organizar_documentos_local.json`,
`chamada_ollama_local.json`. Importe em "Workflows -> Import from File".

## Regras

- Nenhum workflow deve automatizar login/envio nas IAs web
  (ChatGPT/Claude/Gemini).
- Nenhum workflow deve usar API paga de IA.
- Nenhum workflow deve expor porta publica nem usar dominio/VPS.
