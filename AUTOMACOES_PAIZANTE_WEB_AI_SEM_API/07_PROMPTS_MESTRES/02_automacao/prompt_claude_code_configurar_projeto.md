# Prompt Mestre: Claude Code - Configurar Projeto Local

## Contexto
Este prompt e destinado ao Claude Code (execucao local de
arquivos/scripts), no computador do Dr. Gustavo Paizante (OAB/MG
180.822), dentro de
`$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API`.

## Papel da IA
Executor(a) local: leitura/escrita de arquivos, criacao de pastas,
execucao de scripts Python/PowerShell, sem nenhuma API paga.

## Limitacoes obrigatorias
- Nunca apague ou sobrescreva arquivos originais sem antes copia-los para
  `10_BACKUPS`.
- Nunca instale dependencia paga, nunca configure VPS/dominio/porta
  publica.
- Sempre use `$env:USERPROFILE` para localizar a pasta do usuario, nunca
  um nome fixo.

## Tarefas exatas
1. Verifique se a estrutura de pastas da central existe; crie o que
   faltar, sem apagar nada existente.
2. Verifique se existe `.venv` em `05_SCRIPTS_PYTHON`; se nao existir,
   crie com `python -m venv .venv` e instale `requirements.txt`.
3. Rode `pytest` em `05_SCRIPTS_PYTHON/tests` e relate o resultado.
4. Relate qualquer pendencia (ferramenta ausente, erro de permissao) em
   `12_RELATORIOS/pendencias.md`, sem interromper a execucao.

## Formato de saida
1. Lista do que foi criado/verificado.
2. Resultado dos testes.
3. Pendencias registradas.
4. Proximos passos sugeridos.
