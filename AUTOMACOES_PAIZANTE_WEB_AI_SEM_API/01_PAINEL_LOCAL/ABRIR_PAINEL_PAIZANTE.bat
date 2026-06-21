@echo off
REM Clique duas vezes neste arquivo (ou no atalho da Area de Trabalho criado
REM por criar_atalho_area_trabalho.ps1) para abrir o Painel Local Automacoes
REM Paizante. Ele inicia o servidor (criando a venv e instalando as
REM dependencias na primeira vez, se necessario) e abre o navegador em
REM http://localhost:8000.

set "PAINEL_DIR=%~dp0"

echo Iniciando o Painel Local Automacoes Paizante...
echo (uma janela do PowerShell vai abrir com o servidor - nao a feche)

start "Painel Paizante - servidor (nao feche esta janela)" powershell -NoExit -ExecutionPolicy Bypass -File "%PAINEL_DIR%run_painel.ps1"

timeout /t 5 /nobreak >nul

start "" "http://localhost:8000"

exit
