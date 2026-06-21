@echo off
title Painel Paizante
setlocal

REM Este arquivo pode ficar direto na Area de Trabalho (ou em qualquer
REM lugar) - ele encontra o hub sozinho, usando %USERPROFILE%. Nao
REM precisa copiar nenhum outro arquivo junto.

set "BASE_DIR=%USERPROFILE%\Documents\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API"
set "PAINEL_DIR=%BASE_DIR%\01_PAINEL_LOCAL"
set "RUN_SCRIPT=%PAINEL_DIR%\run_painel.ps1"

if not exist "%RUN_SCRIPT%" (
    echo Nao encontrei o hub Automacoes Paizante em:
    echo   %BASE_DIR%
    echo.
    echo Confirme que a pasta AUTOMACOES_PAIZANTE_WEB_AI_SEM_API esta em:
    echo   %USERPROFILE%\Documents\
    echo.
    pause
    exit /b 1
)

echo Iniciando o Painel Local Automacoes Paizante...
echo (uma janela do PowerShell vai abrir com o servidor - nao a feche)

start "Painel Paizante - servidor (nao feche esta janela)" powershell -NoExit -ExecutionPolicy Bypass -File "%RUN_SCRIPT%"

timeout /t 5 /nobreak >nul

start "" "http://localhost:8000"

exit
