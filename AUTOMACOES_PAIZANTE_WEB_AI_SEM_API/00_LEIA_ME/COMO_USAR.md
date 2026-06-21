# Como Usar

## Fluxo completo (resumo)

1. Coloque os documentos do caso em
   `04_DOCUMENTOS/entrada/documentos_para_organizar` (ou na subpasta
   especifica: analisar, unir, separar, pecas_para_revisar).
2. Rode o organizador documental (painel ou `python run.py` opcao
   "organizar documentos") para copiar, renomear e indexar os documentos na
   pasta do cliente em `04_DOCUMENTOS/clientes/<nome_do_cliente>/`.
3. Abra o painel local (`http://localhost:8000`) e crie um novo trabalho:
   escolha o tipo de tarefa, o cliente, escreva o resumo do caso e marque
   quais IAs vai usar (ChatGPT, Claude, Gemini).
4. O painel gera um prompt especifico para cada IA escolhida
   (`03_FILAS_DE_TRABALHO/01_para_chatgpt`, `03_para_claude`,
   `05_para_gemini`). Use o botao "copiar para clipboard".
5. Use `02_CHROME_WORKSPACE/abrir_chatgpt.ps1` (ou claude/gemini/todas) para
   abrir a IA no Chrome. Cole o prompt manualmente, revise e envie voce
   mesmo. Nenhum script faz isso por voce.
6. Copie a resposta da IA e cole no campo correspondente do painel (ou
   salve em `03_FILAS_DE_TRABALHO/02_retorno_chatgpt` etc.). O painel
   registra a resposta no trabalho.
7. Repita os passos 4-6 para as demais IAs selecionadas.
8. No painel, clique em "comparar respostas": ele gera um comparativo em
   `03_FILAS_DE_TRABALHO/07_comparacao` com pontos fortes/fracos,
   divergencias e riscos de alucinacao de cada resposta.
9. Clique em "consolidar": gera a versao consolidada e a versao final em
   `03_FILAS_DE_TRABALHO/08_consolidado` e `09_final`.
10. Faca a revisao humana final (sempre obrigatoria) e gere o checklist de
    protocolo. Use "abrir pasta do trabalho" para revisar tudo no
    Explorador de Arquivos.
11. Monte o pacote de protocolo em
    `04_DOCUMENTOS/saida/pacotes_protocolo` quando a peca estiver aprovada.
12. Gere um backup (botao "gerar backup" ou
    `10_BACKUPS`) ao final de cada caso importante.

## Abrindo o painel

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\05_SCRIPTS_PYTHON"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Ou diretamente: `01_PAINEL_LOCAL\run_painel.ps1`.

## Abrindo as IAs

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\02_CHROME_WORKSPACE"
.\abrir_todas_ias.ps1
```

Veja o detalhamento de cada fluxo em `FLUXO_CHATGPT_PLUS_WEB.md`,
`FLUXO_CLAUDE_WEB.md` e `FLUXO_GEMINI_WEB.md`.
