# Ollama Local (opcional)

O Ollama permite rodar modelos de linguagem abertos localmente, de forma
gratuita, sem nenhuma API paga e sem enviar dados para fora do
computador.

## Instalacao (se ausente)

1. Baixe em https://ollama.com/download (Windows).
2. Instale normalmente; o Ollama passa a rodar como servico local na
   porta 11434.
3. Baixe um modelo: `ollama pull llama3.1:8b` (ver
   `modelos_recomendados.md` para outras opcoes).

## Testar

```powershell
cd "$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API\09_OLLAMA_LOCAL"
.\testar_ollama.ps1
```

## Uso

Veja `exemplo_chamada_ollama.json` para o formato de requisicao ao
endpoint local `http://localhost:11434/api/generate`. O Ollama nunca
substitui o fluxo de revisao humana descrito em `00_LEIA_ME`, e nunca
deve ser usado para burlar a ausencia de API paga das demais IAs - ele e
uma ferramenta adicional, gratuita e local, para tarefas simples.

## Chat com IA local no Painel (com anexos)

O Painel Local (`01_PAINEL_LOCAL`) tem uma aba "Chat com IA local" dentro
de cada trabalho (`/trabalho/<id>/chat`), que fala diretamente com o
Ollama instalado na sua maquina:

- Voce pode anexar documentos (PDF, DOCX, TXT) e fotos/imagens.
- A IA local sempre pergunta o que e o anexo e qual e a finalidade antes
  de analisar - ela nunca presume o assunto do caso por conta propria.
- Documentos tem o texto extraido automaticamente; fotos/imagens sao
  enviadas para um modelo com visao, se houver um instalado (ver
  `modelos_recomendados.md`).
- O historico de cada chat fica salvo em
  `01_PAINEL_LOCAL/data/trabalhos/<id>/chat.json` e os anexos em
  `01_PAINEL_LOCAL/data/trabalhos/<id>/anexos/`. "Iniciar novo chat" apenas
  arquiva o historico atual (nunca apaga).
- Se o Ollama nao estiver rodando ou nao tiver nenhum modelo instalado, o
  painel avisa isso na propria tela do chat, sem quebrar o resto do
  sistema.

Continua valendo: a IA local nunca redige a peca final nem substitui a
revisao humana obrigatoria do advogado - ela e apoio para entender
anexos e tarefas simples do dia a dia.
