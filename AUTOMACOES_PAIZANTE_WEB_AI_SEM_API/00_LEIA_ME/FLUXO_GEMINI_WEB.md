# Fluxo Gemini via Web

1. No painel, gere o prompt para Gemini (botao "gerar prompt Gemini").
   Arquivo em `03_FILAS_DE_TRABALHO/05_para_gemini/<id_trabalho>.md`.
2. Copie para clipboard.
3. Rode `02_CHROME_WORKSPACE\abrir_gemini.ps1` para abrir
   https://gemini.google.com numa nova aba.
4. Cole o prompt manualmente. Se a tarefa envolver PDFs grandes ou
   imagens, anexe os arquivos manualmente na conversa (upload manual, com
   autorizacao previa para dados sensiveis - veja
   `LGPD_SIGILO_PROFISSIONAL.md`).
5. Revise e envie voce mesmo.
6. Copie a resposta do Gemini.
7. Volte ao painel, cole no campo "resposta Gemini" e salve. Vai para
   `03_FILAS_DE_TRABALHO/06_retorno_gemini/` e `resposta_gemini.md`.
8. Marque no checklist que o envio foi manual.

Gemini e indicado, neste fluxo, para: processamento de documentos longos,
conteudo multimodal (imagens, PDFs grandes), resumo extenso, extracao de
dados estruturados de varios arquivos e preparacao de resumos para as
demais IAs.
