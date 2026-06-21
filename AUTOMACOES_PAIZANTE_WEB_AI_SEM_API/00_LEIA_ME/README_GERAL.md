# AUTOMACOES_PAIZANTE_WEB_AI_SEM_API

Central de produtividade juridica assistida por IA, 100% local e gratuita,
do Dr. Gustavo Paizante - OAB/MG 180.822.

## O que esta central faz

Organiza documentos do escritorio localmente, gera prompts especificos para
ChatGPT, Claude e Gemini (usados manualmente via navegador), guarda as
respostas dessas IAs, compara essas respostas, consolida a melhor versao e
ajuda a montar a peca juridica final e o pacote de protocolo. Tudo isso
acontece no computador do usuario, sem nenhuma API paga, sem VPS, sem
dominio publico e sem portas abertas para a internet.

## Pasta principal

No Windows, esta central deve viver em:

```
$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API
```

Todos os scripts detectam esse caminho automaticamente via `$env:USERPROFILE`
e nunca assumem um nome fixo de usuario.

## Verificar e instalar tudo de uma vez

Na raiz desta central ha um script unico,
`VERIFICAR_E_INSTALAR_TUDO.ps1`, que confere e corrige o ambiente
inteiro: verifica/instala Python, cria e atualiza o ambiente virtual e
as dependencias do painel, roda a auditoria automatizada (pytest),
verifica/instala Google Chrome e Ollama (IA local opcional), baixa o
modelo de IA local recomendado e recria o atalho da Area de Trabalho. No
final grava um relatorio em `12_RELATORIOS`. Para rodar (PowerShell como
Administrador, recomendado para as instalacoes via winget):

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API"
.\VERIFICAR_E_INSTALAR_TUDO.ps1
```

Nao apaga nem sobrescreve nada do seu trabalho - so confere, instala o
que faltar e relata.

## Estrutura de pastas

- `00_LEIA_ME` - documentacao (este conjunto de arquivos).
- `01_PAINEL_LOCAL` - painel web FastAPI (http://localhost:8000).
- `02_CHROME_WORKSPACE` - scripts que abrem ChatGPT, Claude, Gemini, n8n e o
  painel no Chrome.
- `03_FILAS_DE_TRABALHO` - filas de trabalho em transito entre as IAs
  (para/retorno de cada IA, comparacao, consolidado, final).
- `04_DOCUMENTOS` - entrada de documentos, pastas por cliente e saida de
  documentos gerados.
- `05_SCRIPTS_PYTHON` - codigo Python (FastAPI, ferramentas de PDF/DOCX,
  clipboard, comparacao, consolidacao etc.) e testes automatizados.
- `06_N8N_LOCAL` - n8n rodando localmente via Docker, somente em
  `127.0.0.1:5678`.
- `07_PROMPTS_MESTRES` - prompts juridicos e operacionais prontos para
  colar nas IAs.
- `08_MODELOS_JURIDICOS` - modelos de pecas e instrucoes (procuracao,
  declaracao, hipossuficiencia, contrato de honorarios, INSS, trabalhista,
  mandado de seguranca).
- `09_OLLAMA_LOCAL` - scripts e notas para uso opcional de modelos locais via
  Ollama (gratuito, sem API paga).
- `10_BACKUPS` - copias de seguranca (n8n, documentos, configuracoes,
  prompts, respostas de IA).
- `11_LOGS` - logs de sistema, Python, n8n, Chrome e automacoes.
- `12_RELATORIOS` - diagnostico, instalacao, testes, pendencias e relatorio
  final.

## Princípios inegociaveis

1. **Sem API paga.** ChatGPT, Claude e Gemini sao usados apenas pela
   interface web, com o usuario colando o prompt e clicando em enviar.
2. **Sem infraestrutura publica.** Sem VPS, sem dominio, sem n8n Cloud, sem
   portas expostas para a internet. Tudo em `127.0.0.1`/`localhost`.
3. **Sem automacao de login, envio ou burla.** Nenhum script preenche
   senha, clica em "enviar" dentro do chat das IAs, captura cookie/token,
   ou tenta contornar CAPTCHA, 2FA ou limites de uso.
4. **Sigilo profissional e LGPD.** Documentos sensiveis de clientes só sao
   enviados a uma IA externa apos decisao humana explicita. Veja
   `LGPD_SIGILO_PROFISSIONAL.md`.
5. **Criar, nunca destruir.** Os scripts desta central nunca apagam ou
   sobrescrevem arquivos originais; sempre trabalham em copias.
6. **Assinatura padrao.** Toda peca juridica final gerada com apoio desta
   central termina com: `Dr. Gustavo Paizante - OAB/MG 180.822`.

## Por onde comecar

Leia, nesta ordem: `COMO_USAR.md`, `LIMITES_SEM_API.md`,
`FLUXO_CHATGPT_PLUS_WEB.md` / `FLUXO_CLAUDE_WEB.md` / `FLUXO_GEMINI_WEB.md`,
`COMANDOS_PRINCIPAIS.md` e `CHECKLIST_OPERACIONAL.md`.
