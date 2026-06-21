# Pendencias Consolidadas

Lista unica de tudo que precisa de validacao/acao manual no computador
real do usuario (Windows), porque foi gerado em um container Linux na
nuvem e nao pode ser validado neste ambiente.

## Ambiente / diagnostico (FASE 1)

- [ ] Rodar `12_RELATORIOS\diagnostico.ps1` no Windows real para
  confirmar versao do Windows, PowerShell, ExecutionPolicy, presenca de
  Chrome/Git/Node/Docker/Ollama, portas 5678/8000/11434 livres e espaco
  em disco.
- [ ] Confirmar `$env:USERPROFILE` real e que a pasta esta em
  `$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API`.

## Python / painel local

- [ ] Criar a venv, instalar `requirements.txt` e rodar `pytest` no
  Windows real (ja validado com sucesso - 18/18 - no ambiente de
  geracao Linux; ver `12_RELATORIOS/testes.md`).
- [ ] Iniciar o painel (`run_painel.ps1`) e confirmar acesso em
  `http://localhost:8000`.

## Chrome

- [ ] Confirmar que o Google Chrome esta instalado no caminho padrao
  (`C:\Program Files\Google\Chrome\Application\chrome.exe`) ou ajustar
  `02_CHROME_WORKSPACE\_common.ps1` se estiver em outro local.
- [ ] Testar manualmente cada script (`abrir_chatgpt.ps1`,
  `abrir_claude.ps1`, `abrir_gemini.ps1`, `abrir_n8n.ps1`,
  `abrir_painel.ps1`, `abrir_todas_ias.ps1`,
  `abrir_fluxo_juridico.ps1`).

## Docker / n8n local

- [ ] Instalar/abrir o Docker Desktop no Windows.
- [ ] Rodar `06_N8N_LOCAL\start_n8n.ps1` e confirmar subida em
  `http://localhost:5678` com o usuario/senha definidos em `.env`
  (copiar de `.env.example` e trocar a senha padrao
  `troque_esta_senha`).
- [ ] Importar os 7 workflows de `06_N8N_LOCAL\workflows\` manualmente
  pela interface do n8n (import e sempre manual, por design).
- [ ] Confirmar que nenhum container/volume n8n anterior conflita (
  `docker ps -a`, `docker volume ls`).

Neste ambiente de geracao, por coincidencia, o binario Docker estava
disponivel e foi usado apenas para validar a sintaxe de
`docker-compose.yml` (`docker compose config`) e dos 7 JSONs de
workflow - o container nunca foi de fato iniciado, e isso nao substitui
o teste no Windows real do usuario.

## Ollama (opcional)

- [ ] Instalar o Ollama (https://ollama.com) se desejar IA local
  gratuita complementar.
- [ ] Rodar `09_OLLAMA_LOCAL\testar_ollama.ps1` e, se desejado, baixar
  um modelo (`ollama pull llama3.1:8b`, por exemplo).

## Modelos juridicos (papel timbrado)

- [ ] Colocar o arquivo real de papel timbrado do escritorio em
  `08_MODELOS_JURIDICOS\papel_timbrado\` (apenas instrucoes/placeholder
  foram gerados, pois o agente nao tem o arquivo real do usuario).

## Itens que sao SEMPRE manuais (por desenho, nao sao pendencia a "resolver")

- Colar o prompt no ChatGPT/Claude/Gemini e clicar em enviar.
- Login em qualquer um dos servicos de IA.
- Revisao e aprovacao final de qualquer peca juridica pelo
  Dr. Gustavo Paizante - OAB/MG 180.822 antes de uso processual ou
  envio ao cliente.
- Protocolo da peca no sistema do tribunal/orgao competente.
- Qualquer envio de e-mail ao cliente.

## Arquivos de conflito durante a geracao

Nenhum arquivo original foi sobrescrito ou apagado durante a geracao
desta central (modo "criar, nunca destruir" respeitado em 100% das
operacoes). Nenhuma pendencia de conflito de nome de arquivo foi
registrada nesta execucao.
