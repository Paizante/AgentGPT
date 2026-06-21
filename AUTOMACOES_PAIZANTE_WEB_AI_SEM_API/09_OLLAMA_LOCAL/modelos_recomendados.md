# Modelos Recomendados (Ollama Local)

Todos gratuitos, rodando localmente, sem API paga e sem enviar dados
para fora da maquina.

- `llama3.1:8b` - uso geral, bom equilibrio entre qualidade e velocidade.
- `qwen2.5:7b` - bom em portugues e tarefas de resumo/extracao.
- `mistral` - rapido, bom para tarefas simples e resumo curto.
- `phi3` - leve, util em maquinas com menos recursos.
- `codellama` - apoio a tarefas de codigo/scripts locais.

### Para analisar fotos/imagens anexadas no chat do painel

O Chat com IA local do painel (`/trabalho/<id>/chat`) usa automaticamente
um modelo com visao quando voce anexa uma foto ou imagem. Instale pelo
menos um destes:

- `llama3.2-vision:11b` - recomendado, melhor qualidade geral para
  descrever/ler documentos fotografados (precisa de mais RAM/VRAM, ideal
  com 16 GB de RAM ou mais / GPU com 8 GB+ de VRAM).
- `llava:13b` - alternativa com visao, roda em maquinas um pouco mais
  modestas.
- `llava:7b` - versao mais leve, para maquinas com menos recursos
  (8 GB de RAM).

Sem nenhum modelo de visao instalado, o chat continua funcionando para
texto/documentos, mas avisa que nao pode analisar a imagem anexada.

## Instalar um modelo

```powershell
ollama pull llama3.1:8b
ollama pull llama3.2-vision:11b
```

Se a maquina for mais modesta (pouca RAM/sem GPU dedicada), prefira:

```powershell
ollama pull phi3
ollama pull llava:7b
```

## Quando usar Ollama em vez de ChatGPT/Claude/Gemini

Para tarefas simples, repetitivas ou que nao envolvam dados sensiveis de
cliente (ex.: resumir um texto generico, gerar um rascunho rapido), o
Ollama local pode ser suficiente e evita qualquer exposicao de dado fora
da maquina. Para raciocinio juridico complexo, redacao final de peca ou
analise de documentos sensiveis, prefira o fluxo manual via
ChatGPT/Claude/Gemini com revisao humana.
