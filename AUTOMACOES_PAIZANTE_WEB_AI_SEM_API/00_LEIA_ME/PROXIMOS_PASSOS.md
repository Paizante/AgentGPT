# Proximos Passos Sugeridos

1. Copiar esta pasta para
   `$env:USERPROFILE\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API` no
   Windows real (se ainda nao estiver la).
2. Rodar `12_RELATORIOS\diagnostico.ps1` para obter o diagnostico real do
   ambiente Windows.
3. Criar a venv Python e instalar dependencias
   (`05_SCRIPTS_PYTHON/requirements.txt`).
4. Rodar `python run.py` e validar que o painel abre em
   http://localhost:8000.
5. Testar `02_CHROME_WORKSPACE\abrir_todas_ias.ps1` e confirmar que abre
   ChatGPT, Claude e Gemini em abas separadas, sem nenhum preenchimento
   automatico.
6. Se for usar n8n: instalar Docker Desktop, subir
   `06_N8N_LOCAL\start_n8n.ps1` e importar os workflows de exemplo.
7. Se for usar Ollama: instalar o Ollama, baixar um modelo recomendado
   (ex.: `ollama pull llama3.1:8b`) e testar com
   `09_OLLAMA_LOCAL\testar_ollama.ps1`.
8. Criar a primeira pasta de cliente real a partir de
   `04_DOCUMENTOS/clientes/_MODELO_CLIENTE`.
9. Rodar um caso piloto fim a fim (organizar documentos -> criar trabalho
   -> gerar prompts -> usar as 3 IAs -> comparar -> consolidar -> revisar
   -> protocolar) para validar o fluxo completo antes de adotar em massa.
10. Revisar `12_RELATORIOS/pendencias.md` periodicamente e ir fechando os
    itens conforme o ambiente Windows for validado.
