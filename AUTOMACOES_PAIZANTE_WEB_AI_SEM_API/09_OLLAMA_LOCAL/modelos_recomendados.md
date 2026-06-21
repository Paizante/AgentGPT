# Modelos Recomendados (Ollama Local)

Todos gratuitos, rodando localmente, sem API paga e sem enviar dados
para fora da maquina.

- `llama3.1:8b` - uso geral, bom equilibrio entre qualidade e velocidade.
- `qwen2.5:7b` - bom em portugues e tarefas de resumo/extracao.
- `mistral` - rapido, bom para tarefas simples e resumo curto.
- `phi3` - leve, util em maquinas com menos recursos.
- `codellama` - apoio a tarefas de codigo/scripts locais.

## Instalar um modelo

```powershell
ollama pull llama3.1:8b
```

## Quando usar Ollama em vez de ChatGPT/Claude/Gemini

Para tarefas simples, repetitivas ou que nao envolvam dados sensiveis de
cliente (ex.: resumir um texto generico, gerar um rascunho rapido), o
Ollama local pode ser suficiente e evita qualquer exposicao de dado fora
da maquina. Para raciocinio juridico complexo, redacao final de peca ou
analise de documentos sensiveis, prefira o fluxo manual via
ChatGPT/Claude/Gemini com revisao humana.
