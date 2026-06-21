# Meta-Prompt: Roteiro de Execucao para Claude Code

## Contexto
Geracao de um roteiro de execucao passo a passo para o Claude Code
realizar uma tarefa tecnica local (arquivos, scripts, pastas, PDFs,
DOCX, planilhas, backups, relatorios) na central do Dr. Gustavo
Paizante (OAB/MG 180.822).

## Papel da IA
Planejador(a) de execucao tecnica local.

## Dados de entrada
- Objetivo tecnico a alcancar:
- Pastas/arquivos envolvidos (caminhos dentro da central):
- Restricoes (nunca apagar original, sempre logar, sem API paga, sem
  porta publica):

## Tarefas exatas
1. Quebre o objetivo em passos tecnicos concretos e ordenados.
2. Para cada passo, indique a acao exata (criar pasta, copiar arquivo,
   rodar script, gerar relatorio) e o caminho/comando envolvido.
3. Indique, para cada passo, como validar que funcionou (o que checar
   depois).
4. Aponte riscos (ex.: sobrescrever arquivo, dependencia ausente) e como
   evita-los (ex.: copiar para `10_BACKUPS` antes).

## Formato de saida
1. Lista numerada de passos tecnicos (acao -> caminho/comando ->
   validacao).
2. Riscos e mitigacoes.
3. Resultado esperado final.
