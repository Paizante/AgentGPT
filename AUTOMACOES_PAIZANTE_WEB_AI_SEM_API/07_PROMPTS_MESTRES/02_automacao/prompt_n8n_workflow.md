# Prompt Mestre: Criar Workflow n8n Local

## Contexto
Criacao de um workflow n8n 100% local (`127.0.0.1:5678`, sem VPS/dominio),
para automatizar uma tarefa operacional do escritorio do Dr. Gustavo
Paizante (OAB/MG 180.822).

## Papel da IA
Especialista em automacao n8n local, sem uso de APIs pagas de IA dentro
do workflow.

## Dados de entrada
- Objetivo da automacao:
- Gatilho (manual, agendado, webhook local, watcher de pasta):
- Etapas desejadas (em ordem):
- Pastas/arquivos envolvidos (caminhos dentro da central):

## Limitacoes obrigatorias
- Nao automatize login, envio de prompt ou upload nas IAs web
  (ChatGPT/Claude/Gemini) - isso continua manual.
- Nao use credenciais de servico pago de IA.
- Use apenas nodes nativos do n8n e, no maximo, chamadas HTTP para o
  Ollama local (`http://localhost:11434`) quando fizer sentido.

## Tarefas exatas
1. Desenhe o fluxo de nodes (gatilho -> etapas -> saida) em formato
   textual, node a node, com a funcao de cada um.
2. Gere o JSON do workflow n8n correspondente, pronto para importar.
3. Liste o que precisa ser configurado manualmente (caminhos de pasta,
   credenciais locais).

## Formato de saida
1. Descricao do fluxo node a node.
2. JSON do workflow.
3. Passos de configuracao manual.
4. Riscos/limitacoes do workflow proposto.
