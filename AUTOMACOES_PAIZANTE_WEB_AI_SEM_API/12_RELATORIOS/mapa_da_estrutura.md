# Mapa da Estrutura Gerada

Pasta principal (deteccao automatica, sem nome de usuario fixo):
`$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API`

Total de arquivos gerados nesta execucao: **135** (sem contar pastas
vazias de fila/documentos/backups/logs, que existem como estrutura
pronta para uso).

| Pasta | Arquivos | Conteudo |
|---|---|---|
| `00_LEIA_ME/` | 12 | Documentacao geral: README, como usar, limites sem API, LGPD/sigilo, fluxos por IA, comandos principais, checklist operacional, proximos passos. |
| `01_PAINEL_LOCAL/` | 12 | Painel FastAPI local (app, templates, static, data, script de execucao). |
| `02_CHROME_WORKSPACE/` | 10 | Scripts PowerShell para abrir ChatGPT/Claude/Gemini/n8n/painel no Chrome, sempre manual. |
| `03_FILAS_DE_TRABALHO/` | 0 (9 subpastas) | Filas de trabalho espelhadas (para/retorno de cada IA, comparacao, consolidado, final). |
| `04_DOCUMENTOS/` | 0 (estrutura completa) | `entrada/` (9 subpastas), `clientes/_MODELO_CLIENTE/` (13 subpastas numeradas), `saida/` (7 subpastas). |
| `05_SCRIPTS_PYTHON/` | 29 | Pacote `src/` (19 modulos), `tests/` (7 arquivos, 18 testes), `requirements.txt`, `run.py`, README. |
| `06_N8N_LOCAL/` | 16 | `docker-compose.yml`, scripts de start/stop/restart/logs/status/backup, `.env.example`, README, 7 workflows JSON validados. |
| `07_PROMPTS_MESTRES/` | 35 | Prompts mestres organizados em 8 subpastas (juridico, automacao, documentos, videos, comunicacao, planejamento, comparacao entre IAs, meta-prompts). |
| `08_MODELOS_JURIDICOS/` | 9 | Instrucoes para papel timbrado, procuracoes, declaracoes, hipossuficiencia, contratos de honorarios, requerimentos INSS, reclamacoes trabalhistas, mandado de seguranca, modelos base. |
| `09_OLLAMA_LOCAL/` | 4 | Script de teste, exemplo de chamada, modelos recomendados, README. |
| `10_BACKUPS/` | 0 (5 subpastas prontas) | `documentos/`, `prompts/`, `respostas_ias/`, `n8n/`, `configuracoes/`. |
| `11_LOGS/` | 3 (+ subpastas) | `python/`, `chrome/`, `n8n/`, `automacoes/`, `sistema/`. |
| `12_RELATORIOS/` | 5 | `diagnostico.md` (+ `.ps1`), `testes.md`, `instalacao.md`, `pendencias.md`, `mapa_da_estrutura.md` (este arquivo). `relatorio_final.md` sera adicionado ao final da FASE 18. |

## Pastas internas detalhadas

### `04_DOCUMENTOS/clientes/_MODELO_CLIENTE/` (13 subpastas, copiadas para cada novo cliente)

```
01_Documentos_Originais
02_Documentos_Pessoais
03_Comprovantes
04_Documentos_Medicos
05_Documentos_Trabalhistas
06_Procuracao_e_Contratos
07_Hipossuficiencia
08_Requerimentos
09_Pecas_Geradas
10_Comparacao_IAs
11_Consolidado
12_Protocolo
13_Backups
```

### `03_FILAS_DE_TRABALHO/` (9 subpastas)

```
01_para_chatgpt
02_retorno_chatgpt
03_para_claude
04_retorno_claude
05_para_gemini
06_retorno_gemini
07_comparacao
08_consolidado
09_final
```

### `07_PROMPTS_MESTRES/` (8 subpastas, 35 arquivos)

```
01_juridico/            9 arquivos
02_automacao/           5 arquivos
03_documentos/          5 arquivos
04_videos/              4 arquivos
05_comunicacao/         2 arquivos
06_planejamento/        1 arquivo
07_comparacao_ias/      5 arquivos
08_meta_prompts/        4 arquivos
```

## Origem dos dados de cada trabalho (job)

A pasta canonica (fonte de verdade) de cada trabalho criado pelo
painel/CLI e:

```
01_PAINEL_LOCAL/data/trabalhos/<job_id>/
```

contendo `metadata.yaml`, `contexto.md`, `prompt_<ia>.md`,
`resposta_<ia>.md`, `comparativo.md`, `consolidado.md`, `final.md`,
`checklist.md` e `log.md`. Esses mesmos arquivos sao espelhados em
`03_FILAS_DE_TRABALHO/` apenas para visibilidade operacional rapida
(ex.: abrir a pasta da fila e ver tudo que esta pendente para o
ChatGPT, por exemplo).
