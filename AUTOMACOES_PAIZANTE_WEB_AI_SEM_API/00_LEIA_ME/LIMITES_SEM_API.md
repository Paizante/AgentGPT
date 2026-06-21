# Limites: Por que "SEM API" e o que isso significa na pratica

## Regra central

Esta central **nunca** usa API paga de IA (OpenAI, Anthropic, Google
Gemini API, etc.). Todo uso de ChatGPT, Claude e Gemini acontece pela
interface web normal, no navegador, com login manual do usuario e com o
usuario colando e enviando o prompt com as proprias maos.

## O que isso implica

- **ChatGPT** é usado em https://chatgpt.com (conta ChatGPT Plus ou
  gratuita do usuario). A central apenas abre a aba e copia o prompt para
  a area de transferencia; quem cola e clica em enviar e o usuario.
- **Claude** é usado em https://claude.ai pelo navegador, da mesma forma.
- **Gemini** é usado em https://gemini.google.com pelo navegador, da
  mesma forma.
- **Claude Code** (este proprio assistente, quando usado localmente pelo
  usuario) e o "executor local": le, organiza e processa arquivos, roda
  scripts Python, gera relatorios, monta workflows n8n e PDFs/DOCX/planilhas
  diretamente no disco do usuario, sem precisar de API paga adicional.
- **n8n** roda local, em Docker, escutando apenas em `127.0.0.1:5678`. Sem
  conta n8n Cloud, sem dominio, sem tunel publico.
- **Ollama** (opcional) permite rodar modelos abertos localmente
  (llama3.1, qwen2.5, mistral, phi3, codellama) para tarefas simples que
  nao exigem ChatGPT/Claude/Gemini, sem custo e sem enviar dados para fora
  da maquina.

## O que NUNCA é automatizado

- Login ou preenchimento de senha em qualquer site.
- Clique no botao de enviar dentro do chat de uma IA.
- Upload de documento sensivel sem autorizacao humana explicita para
  aquele envio especifico.
- Envio de e-mail, protocolo judicial/administrativo ou peticionamento.
- Captura de cookie, token de sessao ou senha.
- Qualquer tentativa de burlar CAPTCHA, autenticacao em duas etapas (2FA)
  ou limites de uso/rate limit das plataformas.

## Por que funciona assim

O objetivo e ganho de produtividade com seguranca: a central prepara o
contexto, organiza os documentos e gera o prompt certo para a IA certa,
mas a decisao de enviar, o que enviar e quando enviar e sempre humana.
Isso preserva o sigilo profissional, cumpre a LGPD e evita qualquer risco
de violar os termos de uso das plataformas de IA.
