# Fluxo n8n Local

1. Suba o n8n local com `06_N8N_LOCAL\start_n8n.ps1` (usa
   `docker-compose.yml`, bind em `127.0.0.1:5678`, sem dominio/VPS).
2. Acesse http://localhost:5678 no navegador (use
   `02_CHROME_WORKSPACE\abrir_n8n.ps1`).
3. Importe os workflows de exemplo em `06_N8N_LOCAL/workflows/` (novo
   trabalho, checklist documental, rotina de backup, registrar resposta de
   IA, relatorio diario, organizar documentos, chamada Ollama local).
4. Use esses workflows para automatizar tarefas puramente locais: mover
   arquivos, gerar checklists, disparar backups, registrar respostas que
   voce ja colou manualmente, ou chamar o Ollama local. O n8n **nao**
   deve ser usado para automatizar login/envio nas IAs web.
5. Pare o n8n com `stop_n8n.ps1` quando nao estiver em uso, e gere backups
   periodicos com `backup_n8n.ps1`.
