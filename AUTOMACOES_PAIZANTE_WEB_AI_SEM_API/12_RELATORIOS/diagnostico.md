# Diagnostico do Ambiente

## Aviso importante sobre esta geracao

Esta central foi gerada a partir de um agente de codigo executando em um
container Linux efemero na nuvem (ambiente de desenvolvimento do
repositorio), **nao** no PC Windows do usuario. Por isso, os testes reais de
Chrome, Docker, Ollama, portas locais etc. nao puderam ser executados aqui.

O script `12_RELATORIOS/diagnostico.ps1` foi criado e e funcional. Para obter
o diagnostico real do seu computador, copie a pasta
`AUTOMACOES_PAIZANTE_WEB_AI_SEM_API` para
`$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API` no Windows e
execute:

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\12_RELATORIOS"
.\diagnostico.ps1
```

O script vai sobrescrever este arquivo com os dados reais da sua maquina
(versao do Windows, Python, Git, Node, Docker, Ollama, Chrome, portas
5678/8000/11434, espaco em disco, permissao de escrita e containers/volumes
n8n antigos), usando try/catch em cada verificacao para nunca interromper a
execucao por causa de uma ferramenta ausente.

## Resultado da verificacao no ambiente de geracao (container Linux)

| Item | Status | Observacao |
|---|---|---|
| Sistema operacional | Linux (container efemero) | Script final roda no Windows real |
| $env:USERPROFILE | N/A neste container | Use o script no Windows para detectar |
| PowerShell | Nao disponivel neste container | Pendencia de execucao no Windows |
| chrome.exe | Nao verificavel aqui | Pendencia de execucao no Windows |
| Python/pip | Disponiveis no container (usados para montar o projeto) | Validar tambem no Windows |
| Git | Disponivel | OK |
| Node/npm | Nao verificado | Nao critico para este projeto (sem frontend Node) |
| Docker/Docker Compose | Nao verificavel aqui | Pendencia de execucao no Windows |
| Ollama | Nao verificavel aqui | Pendencia de execucao no Windows |
| Tailscale | Nao verificavel aqui | Nao obrigatorio (uso 100% local) |
| Portas 5678/8000/11434 | Nao verificaveis aqui | Verificar no Windows antes de iniciar n8n/painel/Ollama |
| Container/volume n8n antigo | Nao verificavel aqui | Verificar com `docker ps -a` / `docker volume ls` no Windows |

## Pendencias registradas

- [ ] Executar `diagnostico.ps1` no Windows real do usuario para obter o
  diagnostico definitivo.
- [ ] Confirmar presenca de Chrome, Docker, Ollama e Node no ambiente real.
- [ ] Confirmar que as portas 5678 (n8n), 8000 (painel) e 11434 (Ollama)
  estao livres antes de iniciar os servicos.
- [ ] Verificar se ha container/volume n8n de uma instalacao anterior antes
  de subir um novo `docker-compose.yml`.

Veja também `12_RELATORIOS/pendencias.md` para a lista consolidada de
pendências de todas as fases.
