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
